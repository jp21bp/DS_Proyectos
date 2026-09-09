"""
This file will create the data preprocessing and TF models

Data preprocessing doesn't need validation set because there isn't labels

Recall: the ratio sharpe is being maximized
    Where the ratio sharpe is seen as part of the model loss function

Reason for maximizing ratio sharpe and not returns:
    Ratio sharpe takes into consideration the volatility
"""
#### Importing libraries
import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import os, pickle, copy
from tqdm import tqdm

#### Data path
data_path = os.path.join(
    os.getcwd(),
    '2_OptimizacionPortafolio',
    'Data'
)

#### Reading data
df_tech_indicators = pd.read_csv(
    f'{data_path}/technical_indicators.csv',
    parse_dates=['Date'],
    index_col='Date'
)

#### Creating simple return
    # NOT one of the indicators
y_all_prices = df_tech_indicators.filter(regex="^Price")
y_all_simple_rets = y_all_prices.pct_change()


#### Global hyperparams
WINDOW_SIZE = 50
NUM_STOCKS = 21
STOCK_NAMES = [stock for indicator, stock in \
               df_tech_indicators.columns[:21].str.split("_")]
SEED = 42
np.random.seed(SEED)
tf.random.set_seed(SEED)
LEARN_RATE = 0.001

#################################################
    # Performance Metrics #
##### Function
def performance_metrics(ds_port_returns: pd.Series, periodic_rate: int = 252) -> dict:
    # "ds_port_returns".shape = (num_days,)
    assert type(ds_port_returns) == pd.Series
    # Base Case
    if ds_port_returns.size == 0:
        return {
            "Annualized Return": 0.0,
            "Annualized Volatility": 0.0,
            "Sharpe Ratio": 0.0,
            "Downside Deviation": 0.0,
            "Sortino Ratio": 0.0,
            "Max Drawdown": 0.0,
            "Percent Positive Returns": 0.0,
            "Profit Loss Ratio": 0.0,
            "Cumulative Returns": np.array([1.0])
        }
    
    # Annualize return
    mean_daily_ret = ds_port_returns.mean()
    annualized_ret = mean_daily_ret * periodic_rate

    # Annualized volatility
    vol_daily_ret = ds_port_returns.std()
    annualized_vol = vol_daily_ret * np.sqrt(periodic_rate)
    
    # Sharpe ratio
    annualized_sharpe = annualized_ret/(annualized_vol + 1e-8)

    # Downside deviation
    neg_rets = ds_port_returns[ds_port_returns < 0]
    annualized_downside_dev = neg_rets.std() * np.sqrt(periodic_rate)\
        if len(neg_rets) > 0 else 0.0

    # Sortino ratio
    annualized_sortino = annualized_ret/(annualized_downside_dev + 1e-8)\
        if annualized_downside_dev > 0.0 else 0.0

    # Cumulative returns
    cumulative_rets = (1 + ds_port_returns).cumprod()

    # Max Drawdown
    peak = np.maximum.accumulate(cumulative_rets.values)
    drawdown = (cumulative_rets - peak)/(peak + 1e-8)
    max_drawdown = np.min(drawdown) if len(drawdown) > 0 else 0.0

    # Percentage of positive returns
    per_pos_rets = (len(ds_port_returns[ds_port_returns > 0])/ ds_port_returns.shape[0]) * 100 \
        if len(ds_port_returns) > 0 else 0.0

    # P/L Ratio
    pos_rets = ds_port_returns[ds_port_returns > 0]
    neg_rets = ds_port_returns[ds_port_returns < 0]
    avg_profit = pos_rets.mean() if len(pos_rets) > 0 else 0.0
    avg_loss = neg_rets.mean() if len(neg_rets) > 0 else 0.0
    pl_ratio = abs(avg_profit/(avg_loss + 1e-8)) if avg_loss < 0.0 else 0.0

    # Results
    return {
        "Annualized Return": annualized_ret,
        "Annualized Volatility": annualized_vol,
        "Sharpe Ratio": annualized_sharpe,
        "Downside Deviation": annualized_downside_dev,
        "Sortino Ratio": annualized_sortino,
        "Max Drawdown": max_drawdown,
        "Percent Positive Returns": per_pos_rets,
        "Profit Loss Ratio": pl_ratio,
        "Cumulative Returns": cumulative_rets
    }


#####################################
    # Pre-processing #
#### General window split
def window_split(
        df_test_train_set: pd.DataFrame,
        type: str
) -> np.ndarray:
    # Set up
    all_inputs = []
    all_labels = []
    num_indicators = int(df_test_train_set.shape[1]/NUM_STOCKS)
        # Will be used for the y-label of ech window
    # if type == 'test': # Debug continuity
    #     print(f'start: {df_test_train_set.iloc[0].name}; end: {df_test_train_set.iloc[-1].name}')


    # Splits
    for t in tqdm(
        range(WINDOW_SIZE, df_test_train_set.shape[0]),
        desc=f'IndividualSplits - {type}',
        position=1,
        leave=False
    ):
        # Extracting Data input
        X = df_test_train_set\
            .iloc[t-WINDOW_SIZE: t]
        # Normalizing data input across each technical indicator
        X_norm = pd.DataFrame(
            columns=X.columns,
            index=X.index
        )
        for i in range(num_indicators):
            cols = X.columns[i*NUM_STOCKS: (i+1)*NUM_STOCKS]
            indicator_subset = X[cols]
            subset_vals = indicator_subset.values
            X_norm[cols] = (subset_vals - np.mean(subset_vals)) / \
                (np.std(subset_vals) + np.finfo(float).eps)
        # for i in range(num_indicators):
        #     print('IDXS', X_norm.iloc[0].name, X_norm.iloc[-1].name)
        #     print('MEAN', X_norm[X_norm.columns[i*21:(i+1)*21]].mean(axis=None))
        #     print('STD', X_norm[X_norm.columns[i*21:(i+1)*21]].std(axis=None))
        # Extracting label = future stock final prices of a given day
        y = y_all_simple_rets.iloc[t] 
        # Concatenation
        all_inputs.append(X_norm.values)
        all_labels.append(y.values)

    # Recording dates
        # Useful when graphing model results
    split_label_dates = df_test_train_set.iloc[WINDOW_SIZE: df_test_train_set.shape[0]].index
    # if type =='test': print(split_label_dates[0], split_label_dates[-1])

    # print('DONE')
    return [np.array(all_inputs), np.array(all_labels), split_label_dates.values]

#### Sliding window function
def sliding_window_split(
        df_features: pd.DataFrame,
        train_years: float = 1.0,
        val_years: float = 0.25,
        test_years: float = 1.0,
) -> np.ndarray:
    # Set up
    days_per_year = 252
    train_days = int(train_years * days_per_year)
    val_days = int(val_years * days_per_year)
    test_days = int(test_years * days_per_year)
    train_test_sets = {}
    fullset_counter = 0
    last_day_for_full_set = df_features.shape[0] \
        - test_days - val_days - train_days
    for train_start in tqdm(
        range(0, last_day_for_full_set, test_days - WINDOW_SIZE),
        desc='SlidingTrainTestSplit',
        position=0
    ):
        # Data start dates
        val_start = train_start + train_days
        test_start = val_start + val_days

        # Edge case
        if (test_start + test_days) >  df_features.shape[0]:
            break   # last set runs past avaialble days

        # Extracting data
        df_train_data = df_features\
            .iloc[train_start: train_start + train_days]
        df_val_data = df_features\
            .iloc[val_start: val_start + val_days]
        df_test_data = df_features\
            .iloc[test_start: test_start + test_days]

        # Splitting each set
        train_data_splits = window_split(df_train_data, "train")
        val_data_splits = window_split(df_val_data, "val")
        test_data_splits = window_split(df_test_data, "test")

        # print(
        #     train_data.iloc[0].name,
        #     train_data.iloc[-1].name,
        #     test_data.iloc[0].name,
        #     test_data.iloc[-1].name
        # )

        # Appending data
        train_test_sets[f'fullset{fullset_counter}_train_val_test_list'] = [train_data_splits, val_data_splits, test_data_splits]
        fullset_counter += 1

    return train_test_sets

# dict_sliding_fullsets = sliding_window_split(df_tech_indicators)

#### Expanding window split
def expanding_window_split(
        df_features: pd.DataFrame,
        train_years: float = 1.0,
        val_years: float = 0.25,
        test_years: float = 1.0,
) -> np.ndarray:
    # Set up
    days_per_year = 252
    train_days = int(train_years * days_per_year)
    val_days = int(val_years * days_per_year)
    test_days = int(test_years * days_per_year)
    train_test_sets = {}
    fullset_counter = 0
    last_day_for_full_set = df_features.shape[0] \
        - val_days - test_days 
    for train_end in tqdm(
        range(train_days, last_day_for_full_set, test_days - WINDOW_SIZE),
        desc='ExpandingTrainTestSplit',
        position=0
    ):    
        # Data start dates
        val_start = train_end
        test_start = val_start + val_days

        # Edge case
        if (test_start + test_days) >  df_features.shape[0]:
            break   # last set runs past avaialble days

        # Extracting data
        df_train_data = df_features\
            .iloc[:train_end]
        df_val_data = df_features\
            .iloc[val_start: val_start + val_days]
        df_test_data = df_features\
            .iloc[test_start: test_start + test_days]

        # Splitting each set
        train_data_splits = window_split(df_train_data, "train")
        val_data_splits = window_split(df_val_data, "val")
        test_data_splits = window_split(df_test_data, "test")

        # print(
        #     train_data.iloc[0].name,
        #     train_data.iloc[-1].name,
        #     test_data.iloc[0].name,
        #     test_data.iloc[-1].name
        # )

        # Appending data
        train_test_sets[f'fullset{fullset_counter}_train_val_test_list'] = [train_data_splits, val_data_splits, test_data_splits]
        fullset_counter += 1

    return train_test_sets

# dict_expanding_fullsets = expanding_window_split(df_tech_indicators)










def tmp(arr, ranges):
    """
    Selecciona columnas de un np.ndarray según rangos dados.
    
    Parámetros:
        arr (np.ndarray): Matriz de entrada.
        ranges (list of tuple): Lista de tuplas (inicio, fin) en base 1.
                                 El rango incluye inicio y fin.
    Retorna:
        np.ndarray: Submatriz con las columnas seleccionadas.
    """
    if not isinstance(arr, np.ndarray):
        raise TypeError("El argumento 'arr' debe ser un np.ndarray.")
    if arr.ndim != 2:
        raise ValueError("La matriz debe ser bidimensional.")

    # Convertir rangos base-1 a índices base-0 y combinarlos
    print('START')
    # indices = np.r_[[np.arange(start, end) for start, end in ranges]].flatten()
    indices = np.concatenate([np.arange(start, end) for start, end in ranges])
    # indices=np.array([0,1,2,3,6,7,8])
    print(indices)


    # Validar que los índices estén dentro del rango
    if np.any(indices < 0) or np.any(indices >= arr.shape[1]):
        raise IndexError("Algún índice de columna está fuera de rango.")

    return arr[:, indices]

# Ejemplo de uso
# arr = np.arange(60).reshape(6, 10)  # 6 filas x 10 columnas
# rangos = [(0, 2), (6, 9)]  # 2nda a 4ta y 7ma a 9na columna
# resultado = tmp(arr, rangos)



#### Technical indicator selection
    # Choosing specific indicators instead of all 5
    # Each indicator is 21 cols/stocks long
    # Selection will happen post splits from above
def indicator_selection(list_indicators: list, split_strat: dict):
    ### MAking deep copy
    split_strat_cpy = copy.deepcopy(split_strat)
    ### Mapping: indicator -> corresponding cols
        # Price: 0(inc) - 21(excl)
        # Log Ret: 21 - 42
        # TEMA: 42 - 63
        # HLC3: 63 - 84
        # OBV: 84 - 105
    ranges = []
    for indicator in list_indicators:
        if indicator == 'Price':
            ranges.append((0,21))
        elif indicator == 'LogRet':
            ranges.append((21,42))
        elif indicator == 'TEMA':
            ranges.append((42,63))
        elif indicator == 'HLC3':
            ranges.append((63,84))
        elif indicator == 'OBV':
            ranges.append((84,105))
        else:
            raise TypeError('Indicator not written correctly')
        
    ### Creating col indices
    cols = np.concatenate(
        [np.arange(start, end) for start, end in ranges]
    )

    ### Selecting indicators
    for fullset_key, train_val_test_list in tqdm(
        split_strat_cpy.items(),
        total=len(split_strat_cpy),
        desc='FullsetDict',
        position=0
    ):
        for tvt_set in train_val_test_list:
            # Each tvt_set = [np_inputs, np_labels, np_dates]
            tvt_set[0] = tvt_set[0][:,:,cols]

    return split_strat_cpy


################################################
    # Implementing splits #
#### Implementation
### Sliding strat
sliding_strat_path = f'{data_path}/dict_sliding_strat.pkl'
if os.path.isfile(sliding_strat_path):
    with open(sliding_strat_path, 'rb') as file:
        dict_sliding_fullsets = pickle.load(file)
else:
    dict_sliding_fullsets = sliding_window_split(df_tech_indicators)
    pickle.dump(dict_sliding_fullsets, open(sliding_strat_path, 'wb'))

### Expanding strat
expanding_strat_path = f'{data_path}/dict_expanding_strat.pkl'
if os.path.isfile(expanding_strat_path):
    with open(expanding_strat_path, 'rb') as file:
        dict_expanding_fullsets = pickle.load(file)
else:
    dict_expanding_fullsets = expanding_window_split(df_tech_indicators)
    pickle.dump(dict_expanding_fullsets, open(expanding_strat_path, 'wb'))

### Checking dates
for key, set in dict_expanding_fullsets.items():
    testset = set[2]
    np_dates = testset[2]
    print(np_dates[0], np_dates[-1])



#### Indicator selections
# ### Sliding window
# dict_fullsets_P_L_sliding = \
#     indicator_selection(['Price', 'LogRet'], dict_sliding_fullsets)

# dict_fullsets_H_T_O_sliding = \
#     indicator_selection(['TEMA', 'HLC3', 'OBV'], dict_sliding_fullsets)

dict_fullsets_all_sliding = dict_sliding_fullsets

# ### Expanding window
# dict_fullsets_P_L_expand = \
#     indicator_selection(['Price', 'LogRet'], dict_expanding_fullsets)

# dict_fullsets_H_T_O_expand = \
#     indicator_selection(['TEMA', 'HLC3', 'OBV'], dict_expanding_fullsets)

dict_fullsets_all_expand = dict_expanding_fullsets


#### Chekcing
# dict_fullsets_H_T_O_expand.keys()
# first_fullset = dict_fullsets_H_T_O_expand['fullset0_train_test_tup']
# trainset = first_fullset[0]
# np_inputs = trainset[0]
# np_inputs.shape  #(50, 63) - confirmed






#### Analyzing levels
### Level 1: Type = dict, 
    # Values = 2-list of [dict_trainset, dict_testset]
    # Key = targeted fullset desired
level_1 = dict_sliding_fullsets  # All fullsets
type(level_1)  # dict
len(level_1)    # 24 keys, each value being a 3-list [trainset, valset, testset]
type(level_1['fullset0_train_val_test_list'])   # 3-list of first fullset "fullset0"
type(level_1['fullset0_train_val_test_list'][0])   # list - trainset of first fullset "fullset0"
type(level_1['fullset0_train_val_test_list'][1])   # list - valset of first fullset "fullset0"
type(level_1['fullset0_train_val_test_list'][2])   # list - testset of first fullset "fullset0"
### Level 2: Type = 2-list
level_2 = level_1['fullset0_train_val_test_list'][0]
type(level_2)   #3-list
len(level_2)    #3, for the 3-list [np_all_window_inputs, np_all_window_labels, np_pdDateTime]
type(level_2[0])    # ndarray - all the window inputs
level_2[0].shape    #(202, 50, 105)
type(level_2[1])    # ndarray - 
level_2[1].shape    #(202, 21)
type(level_2[2])    # ndarray(DateTime) - the dates for the labels in this trainset/testset
level_2[2].shape    #(202, )





#####################################################
    # TF Model#
#### Creating initializers
glorot_init = tf.keras.initializers.GlorotUniform(seed=SEED)
orthogonal_init = tf.keras.initializers.Orthogonal(seed=SEED)
zero_init = tf.keras.initializers.Zeros()

#### Creating Model class
class LSTMModel(tf.keras.Model):
    def __init__(
        self, 
        num_indicators, 
        num_assets, 
        **kwargs
    ):
        super(LSTMModel, self).__init__(**kwargs)
        self.num_indicators = num_indicators
        self.num_assets=num_assets
        self.lstm1 = tf.keras.layers.LSTM(
            2 ** int(np.floor(np.log2(num_assets * 10))),
            input_shape = (WINDOW_SIZE, num_indicators * num_assets),
            kernel_initializer = glorot_init,
            recurrent_initializer = orthogonal_init,
            bias_initializer = zero_init,
            return_sequences=True,
            dropout=0.2,
            recurrent_dropout=0.2,
            name="lstm_1"
        )
        self.lstm2 = tf.keras.layers.LSTM(
            2 ** int(np.floor(np.log2(num_assets * 5))),
            kernel_initializer = glorot_init,
            recurrent_initializer = orthogonal_init,
            bias_initializer = zero_init,
            return_sequences=False,
            dropout=0.2,
            recurrent_dropout=0.2,
            name="lstm_2"
        )
        self.dense = tf.keras.layers.Dense(
            num_assets,
            activation='softmax',
            kernel_initializer = glorot_init,
            bias_initializer = zero_init,
            name='dense'
        )

    def call(self, inputs):
        x = self.lstm1(inputs)
        x = self.lstm2(x)
        x = self.dense(x)
        return x

    def build(self):
        dummy_input = tf.zeros((1, WINDOW_SIZE, self.num_indicators * self.num_assets))
        self.call(dummy_input)
        return
    

#### Creating weight resetter
def seed_reset_weights(model):
    tf.keras.backend.clear_session(free_memory=True)
    for layer in model.layers:
        for weight in layer.weights:
            if weight.name == 'kernel':
                weight.assign(glorot_init(shape=weight.shape))
                # weight.assign(tf.ones(shape=weight.shape))
            elif weight.name == 'recurrent_kernel':
                weight.assign(orthogonal_init(shape=weight.shape))
                # weight.assign(tf.ones(shape=weight.shape))
            elif weight.name == 'bias':
                weight.assign(zero_init(shape=weight.shape))
                # weight.assign(tf.ones(shape=weight.shape))
            else:
                print('OTHER WEIGHT TYPE')
    return model

# #### Checking all functions above
# ### Creating model
# model = LSTMModel(num_indicators=2, num_assets=21)
# model.build()
# model.summary()
# ### Changing weights
# model.layers[-1].get_weights()
# seed_reset_weights(model)
# model.layers[-1].get_weights()

##########################################################
    # TF Loss Function #
#### Creating loss class
class MinRS(tf.keras.losses.Loss):
    def __init__(self, name = None, reduction = "mean", dtype=None, **kwargs):
        # Reductions: {None, 'mean_with_sample_weight', 'none', 'sum_over_batch_size', 'mean', 'sum'}
        super(MinRS, self).__init__(name, reduction, dtype, **kwargs)

    def call(self, y_true, y_pred):
        # Recall: y_true_t = smple returns of the 21 stocks in day t
        # tf.print(type(y_true), type(y_pred))
            #Both: <class 'tensorflow.python.framework.ops.SymbolicTensor'>
        # tf.print(tf.shape(y_true), tf.shape(y_pred))  
            #Both: Shape = (batch_size, num_stocks); affected by val_batch_size
        
        # Convert to TF objects
        tf_y_true =tf.convert_to_tensor(y_true, dtype=tf.float32)   # Stock prices
        tf_y_pred =tf.convert_to_tensor(y_pred, dtype=tf.float32)   # Predicted weights
        tf_batch_all_stock_returns = tf.multiply(tf_y_true, tf_y_pred)
        # tf.print(tf.shape(tf_batch_all_stock_returns))  # Shape: (batch_size, num_stocks)

        ## Calculating daily ratio sharpe
            # Reason for daily: labels are daily
        # Daily returns
        days_per_year = float(252)
        batch_port_daily_returns = tf.reduce_sum(tf_batch_all_stock_returns, axis=1)
        # tf.print(tf.shape(day_returns)) #Shape: (batch_size,)
        # Expected returns
        daily_returns_mean = tf.reduce_mean(batch_port_daily_returns)
        annualized_returns_mean = daily_returns_mean * days_per_year
        # tf.print(tf.shape(daily_returns_mean))  #Shape: (,) -> scalar
        # Volatility
        daily_returns_std = tf.math.reduce_std(batch_port_daily_returns)
        annualized_returns_std = daily_returns_std * tf.math.sqrt(days_per_year)
        # tf.print(tf.shape(daily_returns_std))  #Shape: (,) -> scalar

        batch_diario_rs = daily_returns_mean/(daily_returns_std + tf.keras.backend.epsilon())
        # tf.print(batch_diario_rs)
        batch_annualized_rs = annualized_returns_mean/(annualized_returns_std + tf.keras.backend.epsilon())
            # Mucho sesgo por la baja cantidad de batch_size

        return -batch_diario_rs

#########################################################
    # Callback #
#### Creating Callback class
class CustomCallback(tf.keras.callbacks.Callback):
    # MOdelcheckpoint, LearnRateScheduler, ReduceLROnPlateau?, CSVLogger
    # Algo como: 
        # Every 20 epochs:
            # Check if val_loss is lower than 20 epochs ago
                # If yes: continue
                # If no: reduce learn rate
    # Pra model checkpoint:
        # When ctrl + p is pressed: save the current weights, epoch, and fullset num
    def __init__(self, valset, lr_patience = 3, stop_patience = 10, overfit_thresh = 5):
        super(CustomCallback, self).__init__()
        # self.valset = valset
        self.lr_patience = lr_patience
        self.stop_patience = stop_patience
        self.lr_wait = 0
        self.stop_wait = 0
        self.overfit_thresh = overfit_thresh
        self.prev_val_rs = None

    def on_epoch_begin(self, epoch: int, logs = None):
        ### Cambiar el learn rate
        return


    def on_train_batch_end(self, batch: int, logs = None):
        #### HAcer acumulacion de todos los trainset
        return 
    
    def on_test_batch_end(self, batch: int, logs = None):
        ### Hacer acumulacion de todos los valsets???
        # print(type(valset)) 
            #3-list: [ndarr_inputs.shape = (val_windows, 50, 105), ndarr_labels.shape = (val_windows, 21), ndarr_dates]
        # print(valset[0].shape)
            # (13, 50, 105), even though val_batch_size = 8
            # Thus, val_batch_size affects tf.Loss but not tf.Callback
                # Makes sense, cause in tf.Callback the entire valset is fed
        # print('EXAMINANSDO')
        # print(type(batch))
        # print(batch)
        # Probando Valset calculaciones directamente
        # y_pred = self.model(self.valset[0], training=False)
        # stock_returns = y_pred * self.valset[1]
        # day_ret = np.sum(stock_returns, axis=1)
        # daily_mean_ret = np.mean(day_ret)
        # daily_std_ret = np.std(day_ret)
        # rs = daily_mean_ret/(daily_std_ret + 1e-8)
        # print(f'VAL MEAN: {np.mean(rs)}')
        return



    def on_epoch_end(self, epoch: int, logs = None):
        ### Hacer acumulacion de resultados
            # PAra ver si/no cambiar el learn rate
            # Tambien se puede hacer early stopping?

        ##### Hacer val_RS verdadero
        logs = logs or {}
        val_rs = logs.get('val_RS')

        if not self.prev_val_rs:
            self.prev_val_rs = val_rs
            return

        diff_val_rs = val_rs - self.prev_val_rs

        
        # Examinando self.valset

        

        # Extracting the losses
        logs = logs or {}
        val_loss = logs.get('val_loss')
        train_loss = logs.get('loss')
        # print('LOGS')
        # print(logs)
        # Calculating loss diff
        loss_diff = val_loss - train_loss
        print(f'Epoch {epoch}: train_loss={train_loss:.4f}, val_loss={val_loss:.4f}, loss_diff={loss_diff:.4f}')
        # Actions
        if loss_diff > self.overfit_thresh:
            self.wait += 1
            if self.wait >= self.patience:
                print('Early Stopping')
                self.wait = 0
                self.model.stop_training = True
        else: self.wait = 0

#########################################################
    # Custom Metrics #
#### Creating custom RatioSharpe Metric class
class RatioSharpe(tf.keras.metrics.Metric):
    def __init__(self, dtype = None, name = 'RS'):
        super().__init__(dtype, name)
        # self.returns = self.add_weight(
        #     name='port_returns',
        #     shape=(64,),
        #     # initializer=tf.keras.initializers.Constant([]),
        #     initializer='zeros',
        #     dtype=tf.float32
        # )
        # self.returns = []
        self.batch_rs = self.add_weight(
            name='batch_rs', 
            initializer='zeros',
            dtype=tf.float32
        )
        self.count = self.add_weight(
            name='count_batch_iterations', 
            initializer='zeros',
            dtype=tf.float32
        )

    def update_state(self, y_true, y_pred, sample_weight = None):
        # Method is invoked at end of EACH batch
        # tf.print(type(y_true), type(y_pred))
            # Both: <class 'tensorflow.python.framework.ops.SymbolicTensor'>
        # tf.print(tf.shape(y_true), tf.shape(y_pred))
            # Both: (batch_size, num_stocks) ; affected by val_batch_size
        batch_stock_ret_daily = y_pred * y_true
            # Shape: (batch_size, num_stocks)
        batch_port_ret_daily = tf.reduce_sum(batch_stock_ret_daily, axis=1)
            # Shape: (batch_size,)
        batch_rets_mean = tf.reduce_mean(batch_port_ret_daily)
            # Shape: (,)
        batch_rets_std = tf.math.reduce_std(batch_port_ret_daily)
            # Shape: (,)
        batch_rets_rs = batch_rets_mean/(batch_rets_std + tf.keras.backend.epsilon())

        # Update
        # batch_1d_port_ret_daily = tf.reshape(
        #     tf.cast(
        #         batch_port_ret_daily, tf.float32
        #     ), [-1] # Ensure 1d vector
        # )
        # tf.print(batch_1d_port_ret_daily)

        # concat = tf.concat([self.returns, batch_1d_port_ret_daily], axis=0)
        # tf.print(concat.value_index)

        # self.returns.extend(
        #     tf.reshape(concat, [-1]).numpy().tolist()
        # )
        # self.returns.assign(concat)
        # self.returns[(self.count * 32):((self.count + 1.0) * 32)].assign(batch_1d_port_ret_daily)
        # tf.print(self.returns)


        self.batch_rs.assign_add(batch_rets_rs)
        self.count.assign_add(1)

    def result(self):
        # Method is only executed at end of EACH batch
        return self.batch_rs/self.count
            # Por alguna razon es similar, pero no igual, al loss del modelo
                # A pesar de que los 2 tienen las mismas operaciones

    def reset_state(self):
        # Method is invoked at END of training part and validation/test part
        # self.returns.assign(tf.zeros((32,), dtype=tf.float32))
        self.batch_rs.assign(0.0)
        self.count.assign(0.0)



#########################################################
    # Training - Sliding Technique #
##### Model 1 Indicators: Price and Log returns
#### Setup corresponding data

#### Setup Model
# slide_model_1 = LSTMModel(num_indicators=2, num_assets=NUM_STOCKS, name='two_indicators')
# slide_model_1.compile(
#     optimizer=tf.keras.optimizers.Adam(learning_rate=LEARN_RATE),
#     loss=MinRS
# )
# slide_model_1_results = []





#####  Model 2 Indicators: HLC3, TEMA, OBV
# slide_model_2 = LSTMModel(num_indicators=3, num_assets=NUM_STOCKS, name='three_indicators')





#####  Model 3 Indicators: All 5 
#### Setup corresponding data
dict_fullsets_all_sliding = dict_sliding_fullsets
#### Setup model
slide_model_3 = LSTMModel(num_indicators=5, num_assets=NUM_STOCKS, name='all_indicators')
slide_model_3.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=LEARN_RATE),
    loss=MinRS,
    metrics=[RatioSharpe]
        # NEeds to be 'RatioSharpe' and NOT 'RatioSharpe()'
            # The former creates different object for the trainset and valset
            # The latter uses the SAME object for the trainset and valset
)
#### Setup resulting pandas
df_slide_model_3_weight_results = pd.DataFrame(columns=[f'all_indic_{stock}' for stock in STOCK_NAMES])
df_slide_model_3_weight_results.index = pd.to_datetime(df_slide_model_3_weight_results.index)
#### Training
    # FS = FullSet
for FS_name, FS_train_val_test_list in dict_fullsets_all_sliding.items():
    # Setup
    slide_model_3 = seed_reset_weights(slide_model_3)
    trainset = FS_train_val_test_list[0]    #Contains [np_all_inputs, np_all_labels, np_datetime]
    valset = FS_train_val_test_list[1]
    testset = FS_train_val_test_list[2]
    # Callback
    custom_cb = CustomCallback(valset=(valset[0], valset[1]))
    # Training
    history = slide_model_3.fit(
        x=trainset[0],    # All windows' inputs
        y=trainset[1],    # All windows' labels
        batch_size=32,
        epochs=100,
        verbose=2,
        callbacks=custom_cb,
        validation_data=(valset[0], valset[1]),
        shuffle=False,
        # validation_batch_size=8,
    )



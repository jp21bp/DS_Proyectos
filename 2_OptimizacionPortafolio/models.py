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

#### Global hyperparams
WINDOW_SIZE = 50
NUM_STOCKS = 21
SEED = 42
np.random.seed(SEED)
tf.random.set_seed(SEED)
LEARN_RATE = 0.001

#####################################
    # Pre-processing #
#### General window split
def window_split(
        df_test_train_set: pd.DataFrame,
        type: str
) -> np.ndarray:
    # Set up
    splits = {}
    num_indicators = int(df_test_train_set.shape[1]/NUM_STOCKS)
    window_counter = 0
    y_all_prices = df_test_train_set.filter(regex="^Price")
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
        y = y_all_prices.iloc[t] 
        # Concatenation
        splits[f'{type}set_win{window_counter}_input_label_list'] = [X_norm.values, y.values]
        window_counter += 1

    # Recording dates
        # Useful when graphing model results
    split_label_dates = df_test_train_set.iloc[WINDOW_SIZE: df_test_train_set.shape[0]].index
    # if type =='test': print(split_label_dates[0], split_label_dates[-1])

    # print('DONE')
    return [splits, split_label_dates]

#### Sliding window function
def sliding_window_split(
        df_features: pd.DataFrame,
        train_years: float = 1.0,
        test_years: float = 1.0,
) -> np.ndarray:
    # Set up
    days_per_year = 252
    train_days = int(train_years * days_per_year)
    test_days = int(test_years * days_per_year)
    train_test_sets = {}
    fullset_counter = 0
    last_day_for_full_set = df_features.shape[0] \
        - test_days - train_days
    for train_start in tqdm(
        range(0, last_day_for_full_set, test_days - WINDOW_SIZE),
        desc='SlidingTrainTestSplit',
        position=0
    ):
        # Data start dates
        test_start = train_start + train_days

        # Edge case
        if (test_start + test_days) >  df_features.shape[0]:
            break   # last set runs past avaialble days

        # Extracting data
        df_train_data = df_features\
            .iloc[train_start: train_start + train_days]
        df_test_data = df_features\
            .iloc[test_start: test_start + test_days]

        # Splitting each set
        train_data_splits = window_split(df_train_data, "train")
        test_data_splits = window_split(df_test_data, "test")

        # print(
        #     train_data.iloc[0].name,
        #     train_data.iloc[-1].name,
        #     test_data.iloc[0].name,
        #     test_data.iloc[-1].name
        # )

        # Appending data
        train_test_sets[f'fullset{fullset_counter}_train_test_list'] = [train_data_splits, test_data_splits]
        fullset_counter += 1

    return train_test_sets

# dict_sliding_fullsets = sliding_window_split(df_tech_indicators)

#### Expanding window split
def expanding_window_split(
        df_features: pd.DataFrame,
        train_years: float = 1.0,
        test_years: float = 1.0,
) -> np.ndarray:
    # Set up
    days_per_year = 252
    train_days = int(train_years * days_per_year)
    test_days = int(test_years * days_per_year)
    train_test_sets = {}
    fullset_counter = 0
    last_day_for_full_set = df_features.shape[0] \
        - test_days 
    for train_end in tqdm(
        range(train_days, last_day_for_full_set, test_days - WINDOW_SIZE),
        desc='ExpandingTrainTestSplit',
        position=0
    ):    
        # Data start dates
        test_start = train_end

        # Edge case
        if (test_start + test_days) >  df_features.shape[0]:
            break   # last set runs past avaialble days

        # Extracting data
        df_train_data = df_features\
            .iloc[:train_end]
        df_test_data = df_features\
            .iloc[test_start: test_start + test_days]

        # Splitting each set
        train_data_splits = window_split(df_train_data, "train")
        test_data_splits = window_split(df_test_data, "test")

        # print(
        #     train_data.iloc[0].name,
        #     train_data.iloc[-1].name,
        #     test_data.iloc[0].name,
        #     test_data.iloc[-1].name
        # )

        # Appending data
        train_test_sets[f'fullset{fullset_counter}_train_test_tup'] = [train_data_splits, test_data_splits]
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
    for fullset_key, train_test_tup_value in tqdm(
        split_strat_cpy.items(),
        total=len(split_strat_cpy),
        desc='FullsetDict',
        position=0
    ):
        # print('ONE')
        # print(type(train_test_tup_value))
        for wind_datetime_tup in train_test_tup_value:
            # print('two')
            # print(type(wind_datetime_tup))
            # print(type(wind_datetime_tup[0]))
            for wind_key, wind_tup in wind_datetime_tup[0].items():
                # print('three')
                # print(type(wind_tup))
                wind_tup[0] = wind_tup[0][:, cols]

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

#### SAmple indictor select
indicators = ['Price', 'HLC3']
fullsets_price_HLC3_dict = \
    indicator_selection(indicators, dict_sliding_fullsets)
## Checking
first_fullset = fullsets_price_HLC3_dict['fullset0_train_test_list']
trainset = first_fullset[0]
winds_dict = trainset[0]
first_wind_inputs_labels = winds_dict['trainset_win0_input_label_list']
first_win_inputs = first_wind_inputs_labels[0]
first_win_inputs.shape  #(50, 42) - confirmed





### Expanding strat
expanding_strat_path = f'{data_path}/dict_expanding_strat.pkl'
if os.path.isfile(expanding_strat_path):
    with open(expanding_strat_path, 'rb') as file:
        dict_expanding_fullsets = pickle.load(file)
else:
    dict_expanding_fullsets = expanding_window_split(df_tech_indicators)
    pickle.dump(dict_expanding_fullsets, open(expanding_strat_path, 'wb'))





#### Indicator selections
### Sliding window
dict_fullsets_P_L_sliding = \
    indicator_selection(['Price', 'LogRet'], dict_sliding_fullsets)

dict_fullsets_H_T_O_sliding = \
    indicator_selection(['TEMA', 'HLC3', 'OBV'], dict_sliding_fullsets)

dict_fullsets_all_sliding = dict_sliding_fullsets

### Expanding window
dict_fullsets_P_L_expand = \
    indicator_selection(['Price', 'LogRet'], dict_expanding_fullsets)

dict_fullsets_H_T_O_expand = \
    indicator_selection(['TEMA', 'HLC3', 'OBV'], dict_expanding_fullsets)

dict_fullsets_all_expand = dict_expanding_fullsets









#### Analyzing levels
### Level 1: Type = dict, 
    # Values = 2-list of [dict_trainset, dict_testset]
    # Key = targeted fullset desired
level_1 = dict_sliding_fullsets  # All fullsets
type(level_1)  # dict
len(level_1)    # 24 keys, each value being a 2-list [trainset, testset]
type(level_1['fullset0_train_test_tup'])   # 2-list of first fullset "fullset0"
type(level_1['fullset0_train_test_tup'][0])   # list - trainset of first fullset "fullset0"
type(level_1['fullset0_train_test_tup'][1])   # list - testset of first fullset "fullset0"
### Level 2: Type = 2-list
level_2 = level_1['fullset0_train_test_tup'][0]
type(level_2)   #2-list
len(level_2)    #2, for the 2-list [dict_window_splits, pd.Datetime]
type(level_2[0])    # dict - inputs and labels split for this train set
type(level_2[1])    # pd.DateTimeIndex - the dates for the labels in this trainset/testset
### Level 3: Type = dict
    # Values = tuple of (np_window_inputs, np_window_label)
    # keys = targeted window desired 
level_3 = level_2[0]
type(level_3)   #dict
len(level_3)    #202 windows, each holding 2-list [inputs_ndarray_shape(50,105), label_ndarray_shape(21,)]
type(level_3['trainset_win0_input_label_tup'])  #2-list (of ndarrays) of first window
type(level_3['trainset_win0_input_label_tup'][0])  #ndarray - inputs of first window "win0"
type(level_3['trainset_win0_input_label_tup'][1])  #ndarray - label of first window "win0"
level_3.keys()
### Level 4.1: Type = ndarray
    # Inputs of first window
level_4_1 = level_3['trainset_win0_input_label_tup'][0]
type(level_4_1)   #ndarray
level_4_1.shape   #(50, 105)
    # shape[0] = specific day in the window
        # Doesn't include the last "t" day
    # shape[1] = specific indicator/stock combo
### Level 4.2: Type = ndarray
    # Label of first window
level_4_2 = level_3['trainset_win0_input_label_tup'][1]
type(level_4_2)
level_4_2.shape #(21,)
    # Prices of the 21 stocks on the last "t" day
        # Will be used to calculate the ratio sharpe





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
        dummy_input = tf.zeros((1, WINDOW_SIZE, 2*21))
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
    def __init__(self, name = None, reduction = "sum_over_batch_size", dtype=None):
        super(MinRS, self).__init__(name, reduction, dtype)

    def call(self, y_true, y_pred):
        # Convert to TF objects
        tf_y_true =tf.convert_to_tensor(y_true, dtype=tf.float32)
        tf_y_pred =tf.convert_to_tensor(y_pred, dtype=tf.float32)
        tf_stock_returns = y_true * y_pred

        # Calculating daily ratio sharpe
            # Reason for daily: labels are daily
        day_return = tf.reduce_sum(tf_stock_returns)
        day_std = tf.math.reduce_std(tf_stock_returns)
        day_rs = day_return/(day_std + tf.keras.backend.epsilon())

        return -day_rs

#########################################################
    # Callback #
#### Creating Callback class
class CustomCallback(tf.keras.callbacks.Callback):
    def __init__(self):
        super(CustomCallback, self).__init__()

    def on_predict_batch_end(self, batch, logs = None):
        print(f'Batch: {batch}')
        return

    def on_predict_end(self, logs = None):
        print('PREDICT')
        return 


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


#########################################################
    # Training - Sliding Technique #
##### Model 1 Indicators: Price and Log returns
#### Setup corresponding data

#### Setup Model
slide_model_1 = LSTMModel(num_indicators=2, num_assets=NUM_STOCKS, name='two_indicators')
slide_model_1.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=LEARN_RATE),
    loss=MinRS
)
slide_model_1_results = []





#####  Model 2 Indicators: HLC3, TEMA, OBV
slide_model_2 = LSTMModel(num_indicators=3, num_assets=NUM_STOCKS, name='three_indicators')





#####  Model 3 Indicators: All 5 
#### Setup corresponding data
dict_spliding_fullsets = dict_spliding_fullsets
#### Setup model
slide_model_3 = LSTMModel(num_indicators=5, num_assets=NUM_STOCKS, name='all_indicators')
slide_model_3.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=LEARN_RATE),
    loss=MinRS
)
slide_model_3_results = []
#### Training
    # FS = FullSet
for FS_name, FS_train_test_tup in dict_spliding_fullsets.items():
    seed_reset_weights(slide_model_3)
    trainset = FS_train_test_tup[0]
    slide_model_3




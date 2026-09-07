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
import os, pickle
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
        range(WINDOW_SIZE, df_test_train_set.shape[0] - 1),
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
        splits[f'{type}set_win{window_counter}_input_label_tup'] = (X_norm.values, y.values)
        window_counter += 1

    # print('DONE')
    return splits

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
        range(0, last_day_for_full_set, test_days),
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
        train_test_sets[f'fullset{fullset_counter}_train_test_tup'] = (train_data_splits, test_data_splits)
        fullset_counter += 1

    return train_test_sets

# dict_spliding_window = sliding_window_split(df_tech_indicators)

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
        range(train_days, last_day_for_full_set, test_days),
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
        train_test_sets[f'fullset{fullset_counter}_train_test_tup'] = (train_data_splits, test_data_splits)
        fullset_counter += 1

    return train_test_sets

# dict_expanding_window = expanding_window_split(df_tech_indicators)

################################################
    # Implementing splits #
#### Implementation
### Sliding strat
sliding_start_path = f'{data_path}/dict_sliding_strat.pkl'
if os.path.isfile(sliding_start_path):
    dict_spliding_fullsets = pickle.load(sliding_start_path)
else:
    dict_spliding_fullsets = sliding_window_split(df_tech_indicators)
    pickle.dump(dict_spliding_fullsets, open(sliding_start_path, 'wb'))


### Expanding strat
expanding_strat_path = f'{data_path}/dict_expanding_strat.pkl'
if os.path.isfile(expanding_strat_path):
    dict_expanding_fullsets = pickle.load(expanding_strat_path)
else:
    dict_expanding_fullsets = expanding_window_split(df_tech_indicators)
    pickle.dump(dict_expanding_fullsets, open(expanding_strat_path, 'wb'))



#### Analyzing levels
### Level 1: Type = dict, 
    # Values = tuples of (dict_trainset, dict_testset)
    # Key = targeted fullset desired
level_1 = dict_spliding_fullsets  # All fullsets
type(level_1)  # dict
type(level_1['fullset0_train_test_tup'])   # 2-tuple (of dicts)
type(level_1['fullset0_train_test_tup'][0])   # dict - trainset of first fullset "fullset0"
type(level_1['fullset0_train_test_tup'][1])   # dict - testset of first fullset "fullset0"
### Level 2: Type = dict
    # Values = tuple of (np_window_inputs, np_window_label)
    # keys = targeted window desired 
level_2 = level_1['fullset0_train_test_tup'][0] #Trainset of fullset0
type(level_2)   # dict
type(level_2['trainset_win0_input_label_tup'])  #2-tuple (of ndarrays)
type(level_2['trainset_win0_input_label_tup'][0])  #ndarray - inputs of first window "win0"
type(level_2['trainset_win0_input_label_tup'][1])  #ndarray - label of first window "win0"
### Level 3.1: Type = ndarray
    # Inputs of first window
level_3_1 = level_2['trainset_win0_input_label_tup'][0]
type(level_3_1)   #ndarray
level_3_1.shape   #(50, 105)
    # shape[0] = specific day in the window
        # Doesn't include the last "t" day
    # shape[1] = specific indicator/stock combo
### Level 3.2: Type = ndarray
    # Label of first window
level_3_2 = level_2['trainset_win0_input_label_tup'][1]
type(level_3_2)
level_3_2.shape #(21,)
    # Prices of the 21 stocks on the last "t" day
        # Will be used to calculate the ratio sharpe





#####################################################
    # TF Model#
##### Creating Model class
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
            return_sequences=True,
            dropout=0.2,
            recurrent_dropout=0.2,
            name="lstm_1"
        )
        self.lstm2 = tf.keras.layers.LSTM(
            2 ** int(np.floor(np.log2(num_assets * 5))),
            return_sequences=False,
            dropout=0.2,
            recurrent_dropout=0.2,
            name="lstm_2"
        )
        self.dense = tf.keras.layers.Dense(
            num_assets,
            activation='softmax',
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

model = LSTMModel(num_indicators=2, num_assets=21)
model.build()
model.layers[-1].get_weights()
model.summary()

#### Resetting all model weights
# https://stackoverflow.com/questions/63435679/reset-all-weights-of-keras-model
# def seed_reset_weights(model):
#     tf.keras.backend.clear_session(free_memory=True)
#     for layer in model.layers:
#         if hasattr(layer, 'kernel_initializer'):
#             layer.set_weights(
#                 layer.kernel_initializer(
#                     shape=tf.shape(layer.kernel),
#                     seed=SEED
#                 )
#             )
#         if hasattr(layer, 'recurrent_initializer'):
#             layer.set_weights(
#                 layer.recurrent_initializer(
#                     tf.shape(layer.recurrent_kernel),
#                     seed=SEED
#                 )
#             )
#         if hasattr(layer, 'bias_initializer'):
#             layer.set_weights(
#                 layer.bias_initializer(
#                     tf.shape(layer.bias),
#                     seed=SEED
#                 )
#             )


# def seed_reset_weights(model):
#     tf.keras.backend.clear_session(free_memory=True)
#     for layer in model.layers:
#         for weight in layer.weights:


# layers = model.layers
# weights_0 = layers[0].weights
# config = layers[0].get_config()
# weights_0_1 = weights_0[1]
# weights_0_1.shape
# weights_0_1.name
# weights_0_1.assign(tf.random.uniform(shape=weights_0_1.shape))
# dir(weights_0_1)


##########################################################
    # TF Loss Function #
#### Creating model class
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


#########################################################
    # Training - Sliding Technique #
##### Model 1 Indicators: Price and Log returns
slide_model_1 = LSTMModel(num_indicators=2, num_assets=NUM_STOCKS, name='two_indicators')



#####  Model 2 Indicators: HLC3, TEMA, OBV
slide_model_2 = LSTMModel(num_indicators=3, num_assets=NUM_STOCKS)







#####  Model 3 Indicators: All 5 
slide_model_3 = LSTMModel(num_indicators=5, num_assets=NUM_STOCKS)






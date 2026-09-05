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
import os
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
NUM_INDICATORS = 5
NUM_STOCKS = df_tech_indicators.shape[1] / NUM_INDICATORS

#####################################
    # Pre-processing #
#### General window split
def window_split(
        df_test_train_set: pd.DataFrame,
) -> np.ndarray:
    # Set up
    splits = []
    # print(f'First {df_test_train_set.iloc[0].name}')

    # Splits
    for t in tqdm(
        range(WINDOW_SIZE, df_test_train_set.shape[0] - 1),
        desc='IndividualSplits',
        position=1,
        leave=False
    ):
        # Extracting Data input
        X = df_test_train_set\
            .iloc[t-WINDOW_SIZE: t]\
            .values
        # Normalizing data input
            #TODO: normalize across EACH indicator, for all stocks
        norm_X = (X - np.mean(X)) / (np.std(X) + np.finfo(float).eps)
        # Extracting label = future stock final prices of a given day
        y = df_test_train_set.iloc[t].values
        # Concatenation
        combined = np.array([norm_X, y])
        splits.append(combined)
        # print(df_test_train_set.iloc[t].name)

    # print('DONE')
    return np.array(splits)

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
    train_val_test_sets = []
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
        np_train_data_splits = window_split(df_train_data)
        np_test_data_splits = window_split(df_test_data)

        # print(
        #     train_data.iloc[0].name,
        #     train_data.iloc[-1].name,
        #     test_data.iloc[0].name,
        #     test_data.iloc[-1].name
        # )

        # Appending data
        train_val_test_sets.append((np_train_data_splits, np_test_data_splits))

    return train_val_test_sets

sliding_window_split(df_tech_indicators)


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
    train_val_test_sets = []
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
        np_train_data_splits = window_split(df_train_data)
        np_test_data_splits = window_split(df_test_data)

        # print(
        #     train_data.iloc[0].name,
        #     train_data.iloc[-1].name,
        #     test_data.iloc[0].name,
        #     test_data.iloc[-1].name
        # )

        # Appending data
        train_val_test_sets.append((np_train_data_splits, np_test_data_splits))

    return train_val_test_sets

# expanding_window_split(df_tech_indicators)

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
        self.input_layer = tf.keras.layers.InputLayer(
            shape=(WINDOW_SIZE, num_indicators * num_assets),
            name=f'({WINDOW_SIZE}, {num_indicators}*{num_assets})_input'
        )
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
            activation='linear',
            name='dense'
        )

    def call(self, inputs):
        x = self.lstm1(inputs)
        x = self.lstm2(x)
        x = self.dense(x)
        return x

model = LSTMModel(num_indicators=2, num_assets=21)
dummy_input = np.random.rand(1, WINDOW_SIZE, 2*21).astype(np.float32)
model(dummy_input)
model.summary()
model.compile()

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

        # Calculating ratio sharpe
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
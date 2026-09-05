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
        range(WINDOW_SIZE,df_test_train_set.shape[0]),
        desc='IndividualSplits',
        position=1,
        leave=False
    ):
        splits.append(
            df_test_train_set\
                .iloc[t-WINDOW_SIZE: t]\
                .values
        )
        # print(df_test_train_set.iloc[t].name)

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
        desc='TrainTestSplit',
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
        combined_data = np.array([np_train_data_splits, np_test_data_splits])
        train_val_test_sets.append(combined_data)

    # return np.array(train_val_test_sets)

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
    for train_end in tqdm(range(train_days, last_day_for_full_set, test_days)):    
        # Data start dates
        test_start = train_end

        # Edge case
        if (test_start + test_days) >  df_features.shape[0]:
            break   # last set runs past avaialble days

        # Extracting data
        train_data = df_features\
            .iloc[:train_end]
        test_data = df_features\
            .iloc[test_start: test_start + test_days]

        # print(
        #     train_data.iloc[0].name,
        #     train_data.iloc[-1].name,
        #     test_data.iloc[0].name,
        #     test_data.iloc[-1].name
        # )

        # Appending data
        combined_data = np.array([train_data.values, test_data.values])
        train_val_test_sets.append(combined_data)

    return np.array(train_val_test_sets)

# expanding_window_split(df_tech_indicators)





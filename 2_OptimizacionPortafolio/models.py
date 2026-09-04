"""
This file will create the TF models
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
    train_val_test_sets = []
    last_day_for_full_set = df_features.shape[0] \
        - test_days - val_days - train_days
    for train_start in tqdm(range(0, last_day_for_full_set, test_days)):
        # Data start dates
        val_start = train_start + train_days
        test_start = val_start + val_days

        # Edge case
        if (test_start + test_days) >  df_features.shape[0]:
            break   # last set runs past avaialble days

        # Extracting data
        train_data = df_features\
            .iloc[train_start: train_start + train_days]
        val_data = df_features\
            .iloc[val_start: val_start + val_days]
        test_data = df_features\
            .iloc[test_start: test_start + test_days]

        # print(
        #     train_data.iloc[0].name,
        #     train_data.iloc[-1].name,
        #     val_data.iloc[0].name,
        #     val_data.iloc[-1].name,
        #     test_data.iloc[0].name,
        #     test_data.iloc[-1].name
        # )

        train_val_test_sets.append(
            train_data.values,
            val_data.values,
            test_data.values
        )

sliding_window_split(df_tech_indicators)









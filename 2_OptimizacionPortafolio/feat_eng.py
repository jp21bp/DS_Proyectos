"""
Data feature engineering

Focus technical indicators :
* Prices
* Log returns
* TEMA (Triple Exponential Moving Average)
* HLC3 (High Low Close 3-average)
* OBV (On Balance Volume)

Model details:
* Three separate models with the same input structure:
    - Input shape = (t, k * n)
        * t = lookback window = 50 time steps
        * n = number of assets = 21 stocks
        * k = number of tecnical indicators
* Model 1 tecnical indicators (similar to paper)
    - Prices
    - Log returns
* Model 2 tecnical indicators:
    - HLC3
    - OBV
    - TEMA
* Model 3 tecnical indicators:
    - All 5 of the above
* Thus, there will be three different datasets pre-processed
"""
#### Importacion de modulos
import pandas as pd
import numpy as np
from tqdm import tqdm
import scipy
import os

#### Glocal hyperparams
WINDOW_SIZE = 50

#### Reading data
data_path = os.path.join(
    os.getcwd(),
    '2_OptimizacionPortafolio',
    'Data'
)
### Tecnical indicator 1 : Prices
df_prices = pd.read_csv(
    f"{data_path}/filtered_top40.csv",
    parse_dates=['Date'],
    index_col='Date'
)

#### Tecnical indicator 2: log returns
df_log_rets = np.log(df_prices/df_prices.shift(1))

######################################################
    # Tecnical indicator 3: TEMA #
    # TEMA = 3*EMA(p) - 3*EMA(EMA(p)) + EMA(EMA(EMA(p)))
        # EMA = Exponential Moving Average
#### Calculating EMAs
df_ema_1 = df_prices\
    .ewm(span=WINDOW_SIZE, adjust=False)\
    .mean()

df_ema_2 = df_ema_1\
    .ewm(span=WINDOW_SIZE, adjust=False)\
    .mean()

df_ema_3 = df_ema_2\
    .ewm(span=WINDOW_SIZE, adjust=False)\
    .mean()

#### TEMA
df_tema = 3*df_ema_1 - 3*df_ema_2 + df_ema_3


######################################################
    # Complete Top 40 Dataset #
#### Reading full dataset
df_all = pd.read_csv(
    f"{data_path}/raw_top40_complete.csv",
    parse_dates=['Date'],
    index_col='Date'
)





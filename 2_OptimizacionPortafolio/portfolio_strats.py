"""
This file contains the following from the original paper:
* Non-ML portoflio strategies
* Performance Metrics

Details:
* Risk free rate won't be incorporated for simplicity reasons
* Using simple returns, since daily returns will be used for evaluation

Code inspired from:
https://github.com/hskad/Deep-Learning-Based-Portfolio-Optimization/blob/f082b74e90535b128b7d59c44f840faa19dd445c/dl_portfolio_optimization.ipynb
"""
##### Import libraries
import pandas as pd
import numpy as np
from pypfopt.efficient_frontier import EfficientFrontier
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from pypfopt import risk_models
from pypfopt import expected_returns
from scipy.optimize import minimize
import os
from tqdm import tqdm
from functools import reduce

#### Reading data
data_path = os.path.join(
    os.getcwd(),
    '2_OptimizacionPortafolio',
    'Data'
)
df_prices = pd.read_csv(
    f"{data_path}/filtered_top40.csv",
    parse_dates=['Date'],
    index_col='Date'
)

#### Creating simple returns
df_simple_rets = ((df_prices/df_prices.shift(1)) - 1).dropna()

#### Creating dict to capture all portfolio strats
all_port_returns = {}

################################################
    # Volatility scaling on Returns #
    # Used to focus on strategy rather than market volatility
#### Hyperparams
VOL_SCALE = 0.1
WINDOW_SIZE = 50
#### Calculating EWMSD
    # EWMSD = Exponentially Weighted Moving Std. Dev.
df_ewmsd_daily = df_simple_rets\
    .ewm(span=WINDOW_SIZE, adjust=False)\
    .std()
df_ewmsd_annual = df_ewmsd_daily * np.sqrt(252)

#### Scaling EWMSD
df_ewmsd_scaled = (VOL_SCALE/(df_ewmsd_annual + 1e-8)).shift(1)
    # "shift(1)" to prevent look-ahead bias

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


#################################################
    # Fixed allocation strategy #
    # Allocations will be based on sector #
#### Function
def fixed_alloc(df_asset_returns: pd.DataFrame, fixed_weights: np.ndarray, sector: str) -> pd.Series:
    # "df_asset_returns".shape = (num_days, num_assets)
    # "fixed_weights".shape = (num_assets,)
        # These weights are fixed for the entire portfolio
    # return: np_port_rets, with shape = (num_days)
    assert df_asset_returns.shape[1] == fixed_weights.shape[0]

    df_scaled_weights = df_ewmsd_scaled * fixed_weights
    np_port_rets = (df_asset_returns * df_scaled_weights).sum(axis=1)

    # np_port_rets = np.matmul(df_asset_returns, fixed_weights.T)

    assert type(np_port_rets) == pd.Series
    np_port_rets.name = f'FA_{sector}_returns'
        
    return np_port_rets

#### Identifying sectors
### Reading csv with all info about each stock
df_all_assets_info = pd.read_csv(
    f"{data_path}/top40_alphabetized_EN.csv"
)
### Selecting the stocks that passed the filter
df_asset_infos = df_all_assets_info[
    df_all_assets_info['Ticker'].isin(df_prices.columns)
]

#### Setup: Stock and Sector relationship
### Selecting top 4 sectors in amoung stocks
top4_sectors = df_asset_infos['Sector']\
    .value_counts(sort=True, ascending=False)\
    .index.tolist()[:4]
### Mapping sector to the number of stocks in that sector
dict_sector_stock_count = df_asset_infos['Sector']\
    .value_counts().to_dict()
### Mapping the stock to its sector
dict_stock_to_sector = dict(zip(
    df_asset_infos['Ticker'],
    df_asset_infos['Sector']
))

#### Implementation
    # Create a separate allocations for each of the top 4
    # In each allocation, the chosen sector = 60%, rest = 40%
alloc_strat_returns = []
for sector in top4_sectors:
    # Dividing stocks
    num_sect_stock = dict_sector_stock_count[sector]
    num_nonsect_stock = len(df_prices.columns) - num_sect_stock
    # Weight alloc
    sect_weight_alloc = 0.6/num_sect_stock
    nonsect_weight_alloc = 0.4/num_nonsect_stock
    # Creating weight
    weights = []
    for sect in dict_stock_to_sector.values():
        weights.append(
            sect_weight_alloc if sect == sector else nonsect_weight_alloc
        )
    weights = np.array(weights)
    assert np.sum(weights).round(2) == 1.00
    # Implement strategy
    ds_port_ret = fixed_alloc(df_simple_rets, weights, sector).dropna()
    all_port_returns[f'FA_{sector}'] = ds_port_ret

######################################################
    # Mean-Variance Optimization #
#### Function definition
def MVO(df_asset_returns: pd.DataFrame, window : int = 50) -> pd.Series:
    # "df_asset_returns".shape = (num_days, num_assets)
    df_port_returns = pd.Series(name='MVO_returns')

    for t in tqdm(range(window, df_asset_returns.shape[0])):
        # Setup
        window_rets = df_asset_returns.iloc[t-window:t]
        win_mean_rets = window_rets.mean(axis=0)
        win_cov_rets = window_rets.cov()
        # MVO
        ef = EfficientFrontier(win_mean_rets, win_cov_rets)
        try:
            weights = ef.max_sharpe(risk_free_rate=0.0)
            clean_weights = ef.clean_weights()
                # "clean_weights".shape ~ (num_assets,)
            np_clean_weights = np.array(list(clean_weights.values()))
        except:
            np_clean_weights = np.ones(df_asset_returns.shape[1])/ df_asset_returns.shape[1]
        scaled_weights = df_ewmsd_scaled.iloc[t] * np_clean_weights
        # scaled_weights=np_clean_weights

        # Portfolio return
        port_ret = np.dot(df_asset_returns.iloc[t].values, scaled_weights)
        df_port_returns.loc[df_asset_returns.iloc[t].name] = port_ret

    return df_port_returns

#### Implementation
ds_mvo_port_ret = MVO(df_simple_rets).dropna()
all_port_returns['MVO'] = ds_mvo_port_ret

######################################################
    # Maximum Diversification Optimization #
#### Function definition
def MDO(df_asset_returns: pd.DataFrame, window : int = 50) -> pd.Series:
    # "np_asset_returns".shape = (num_days, num_assets)
    num_assets = df_asset_returns.shape[1]
    df_port_returns = pd.Series(name='MDO_returns')
    last_weights = np.ones(num_assets)/num_assets

    for t in tqdm(range(window, df_asset_returns.shape[0])):
        # Setup
        window_rets = df_asset_returns.iloc[t-window:t]
        win_cov_rets = window_rets.cov()
        win_asset_vol = window_rets.std(axis=0)
        win_asset_vol = np.maximum(win_asset_vol, 1e-6)
            #Ensure win_asset_vol > 0
        # Objective function
        def objective(weights : np.ndarray):
            port_vol = np.sqrt(np.dot(weights.T, np.matmul(win_cov_rets, weights)))
            weighted_asset_vol = np.dot(win_asset_vol, weights)
            diversification_ratio = weighted_asset_vol / (port_vol + 1e-8)
            return -diversification_ratio
        # Constraints
        constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1}) # Sum of weights = 1
        bounds = tuple((0, 1) for _ in range(num_assets)) # Weights between 0 and 1
        # Solve optimization problem
        optimal_weights = minimize(
            objective,
            last_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        # Ensure valid weights
        if (not optimal_weights.success) or \
            (np.any(np.isnan(optimal_weights.x))):
            weights = np.ones(num_assets)/ num_assets
        else:
            weights = optimal_weights.x
            weights = weights/np.sum(weights)   #Normalize
        last_weights = weights
        scaled_weights = df_ewmsd_scaled.iloc[t] * weights
        # scaled_weights = weights

        # Portfolio return
        port_ret = np.dot(df_asset_returns.iloc[t], scaled_weights)
        df_port_returns.loc[df_asset_returns.iloc[t].name] = port_ret

    return df_port_returns

#### Implementation
ds_mdo_port_ret = MDO(df_simple_rets).dropna()
all_port_returns['MDO'] = ds_mdo_port_ret


###############################################33
    # Evaluation #
#### Benchmarking
### Reading data
df_bench = pd.read_csv(
    f'{data_path}/raw_splac_prices.csv',
    parse_dates=['Date'],
    index_col='Date'
)
ds_bench_prices = df_bench['Close']
ds_bench_returns = ((ds_bench_prices/ds_bench_prices.shift(1)) - 1).dropna()
### Transformando el index del benchmark
ds_bench_returns.index = ds_bench_returns.index.normalize()

#### Joining data
all_port_returns['Benchmark'] = ds_bench_returns

#### Identifying comons dates
common_dates = reduce(
    lambda x,y: x.intersection(y), 
    [ds.index for ds in all_port_returns.values()]
)

all_port_returns['MDO'].loc[common_dates]

#### All portfolio returns: performance results and graph
### Setup
all_port_results = {}
fig, ax = plt.subplots(figsize=(8,6))
colors = ["#E6194B","#3CB44B", "#FFE119", "#0082C8", "#F58231", "#911EB4",  "#46F0F0"]
### Graph
for i, (strat, ds_port_ret) in enumerate(all_port_returns.items()):
    performance = performance_metrics(ds_port_ret.loc[common_dates])
    all_port_results[strat] = performance
    ax.plot(
        range(len(common_dates)),
        performance['Cumulative Returns'],
        color = colors[i],
        label = strat
    )
ax.set_xticks(range(len(common_dates)))
ax.set_xticklabels(common_dates.date, rotation=90)
ax.xaxis.set_major_locator(MultipleLocator(200))
ax.legend()
plt.show()




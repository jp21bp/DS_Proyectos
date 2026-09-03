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

df_simple_rets = ((df_prices/df_prices.shift(1)) - 1).dropna()

#################################################
    # Performance Metrics #
##### Function
def performance_metrics(np_port_returns: np.ndarray, periodic_rate: int = 252) -> dict:
    # "np_port_returns".shape = (num_days,)
    # Base Case
    if np_port_returns.size == 0:
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
    mean_daily_ret = np.mean(np_port_returns)
    annualized_ret = mean_daily_ret * periodic_rate

    # Annualized volatility
    vol_daily_ret = np.std(np_port_returns)
    annualized_vol = vol_daily_ret * np.sqrt(periodic_rate)
    
    # Sharpe ratio
    annualized_sharpe = annualized_ret/(annualized_vol + 1e-8)

    # Downside deviation
    neg_rets = np_port_returns[np_port_returns < 0]
    annualized_downside_dev = np.std(neg_rets) * np.sqrt(periodic_rate)\
        if len(neg_rets) > 0 else 0.0

    # Sortino ratio
    annualized_sortino = annualized_ret/(annualized_downside_dev + 1e-8)\
        if annualized_downside_dev > 0.0 else 0.0

    # Cumulative returns
    cumulative_rets = np.cumprod(1 + np_port_returns)

    # Max Drawdown
    peak = np.maximum.accumulate(cumulative_rets)
    drawdown = (cumulative_rets - peak)/(peak + 1e-8)
    max_drawdown = np.min(drawdown) if len(drawdown) > 0 else 0.0

    # Percentage of positive returns
    per_pos_rets = (len(np_port_returns[np_port_returns > 0])/ np_port_returns.shape[0]) * 100 \
        if len(np_port_returns) > 0 else 0.0

    # P/L Ratio
    pos_rets = np_port_returns[np_port_returns > 0]
    neg_rets = np_port_returns[np_port_returns < 0]
    avg_profit = np.mean(pos_rets) if len(pos_rets) > 0 else 0.0
    avg_loss = np.mean(neg_rets) if len(neg_rets) > 0 else 0.0
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
def fixed_alloc(np_asset_returns: np.ndarray, fixed_weights: np.ndarray) -> np.ndarray:
    # "np_asset_returns".shape = (num_days, num_assets)
    # "fixed_weights".shape = (num_assets,)
        # These weights are fixed for the entire portfolio
    # return: np_port_rets, with shape = (num_days)
    assert np_asset_returns.shape[1] == fixed_weights.shape[0]

    np_port_rets = np.matmul(np_asset_returns, fixed_weights.T)
        # In numpy: if "tmp" is 1d vector, then no difference
                # between "tmp" and "tmp.T"
            # Only putting "fixed_weights.T" for notation consistency
        
    return np_port_rets

#### Identifying sectors
df_assets_raw = pd.read_csv(
    f"{data_path}/top40_alphabetized_EN.csv"
)
df_asset_infos = df_assets_raw[
    df_assets_raw['Ticker'].isin(df_prices.columns)
]

#### Setup: Ticker and Sector relaton
top4_sectors = df_asset_infos['Sector']\
    .value_counts(sort=True, ascending=False)\
    .index.tolist()[:4]
dict_sector_stock_count = df_asset_infos['Sector']\
    .value_counts().to_dict()
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
    # Implement strategy
    np_port_ret = fixed_alloc(df_simple_rets.values, np.array(weights))
    np_port_ret = np_port_ret[~np.isnan(np_port_ret)]   #Erasing NaNs
    alloc_strat_returns.append(np_port_ret)


######################################################
    # Mean-Variance Optimization #
def MVO(df_asset_returns: np.ndarray, window : int = 50) -> np.ndarray:
    # "np_asset_returns".shape = (num_days, num_assets)
    port_returns = []

    for t in tqdm(range(window, df_asset_returns.shape[0])):
        # Setup
        window_rets = df_asset_returns.iloc[t-window:t]
        # win_mean_rets = expected_returns.mean_historical_return(window_rets)
        # win_cov_rets = risk_models.sample_cov(window_rets)
        win_mean_rets = window_rets.mean(axis=0)
        win_cov_rets = window_rets.cov()
            # "np.cov": rows = variables/stock, cols = observations
        # MVO
        ef = EfficientFrontier(win_mean_rets, win_cov_rets)
        try:
            weights = ef.max_sharpe(risk_free_rate=0.0)
            clean_weights = ef.clean_weights()
                # "clean_weights".shape ~ (num_assets,)
        except:
            weights = np.ones(df_asset_returns.shape[1])/ df_asset_returns.shape[1]
        np_clean_weights = np.array(list(clean_weights.values()))
        # Portfolio return
        port_ret = np.dot(df_asset_returns.iloc[t].values, np_clean_weights)
        port_returns.append(port_ret)

    return np.array(port_returns)

np_mvo_port_ret = MVO(df_simple_rets)


fig, ax = plt.subplots(figsize=(8,6))
dates = df_simple_rets\
    .iloc[-np_mvo_port_ret.shape[0]:]\
    .index.date
results = performance_metrics(np_mvo_port_ret)
ax.plot(
    range(len(dates)),
    results["Cumulative Returns"],
    # color = colors[i],
    label = 'mvo'
)
ax.set_xticks(range(len(dates)))
ax.set_xticklabels(dates, rotation=45)
ax.xaxis.set_major_locator(MultipleLocator(500))
ax.legend()
plt.show()


######################################################
    # Maximum Diversification Optimization #
def MDO(np_asset_returns: np.ndarray, window : int = 50) -> np.ndarray:
    # "np_asset_returns".shape = (num_days, num_assets)
    num_assets = np_asset_returns.shape[1]
    port_returns = []
    last_weights = np.ones(num_assets)/num_assets

    for t in tqdm(range(window, np_asset_returns.shape[0])):
        # Setup
        window_rets = np_asset_returns[t-window:t]
        win_cov_rets = np.cov(window_rets.T)
        win_asset_vol = np.std(np_asset_returns, axis = 0)
        win_asset_vol = np.maximum(win_asset_vol, 1e-6)
            #Ensure win_asset_vol > 0
        # Objective function
        def objective(weights):
            port_vol = np.sqrt(np.dot(weights.T, np.dot(win_cov_rets, weights)))
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
        # Portfolio return
        port_ret = np.dot(np_asset_returns[t], weights)
        port_returns.append(port_ret)

    return np.array(port_returns) 


np_mdo_port_ret = MDO(df_simple_rets.values)


fig, ax = plt.subplots(figsize=(8,6))
dates = df_simple_rets\
    .iloc[-np_mdo_port_ret.shape[0]:]\
    .index.date
results = performance_metrics(np_mdo_port_ret)
ax.plot(
    range(len(dates)),
    results["Cumulative Returns"],
    # color = colors[i],
    label = 'mvo'
)
ax.set_xticks(range(len(dates)))
ax.set_xticklabels(dates, rotation=45)
ax.xaxis.set_major_locator(MultipleLocator(500))
ax.legend()
plt.show()

###############################################33
    # Evaluation #
#### Loading benchmark


#### Evaluation
# dict_performance_results = {}
# fig, ax = plt.subplots(figsize=(8,6))
# colors = ['green', 'blue', 'orange', 'red'], 'purple'
# dates = df_simple_rets\
#     .iloc[-alloc_strat_returns[0].shape[0]:]\
#     .index.date
# for i, np_port_ret in enumerate(alloc_strat_returns):
#     results = performance_metrics(np_port_ret)
#     dict_performance_results[f'{top4_sectors[i]} Heavy'] = results
#     # axs_arr[i].plot(results["Cumulative Returns"])
#     ax.plot(
#         range(len(dates)),
#         results["Cumulative Returns"],
#         color = colors[i],
#         label = f'{top4_sectors[i]} Heavy'
#     )
# ax.set_xticks(range(len(dates)))
# ax.set_xticklabels(dates, rotation=45)
# ax.xaxis.set_major_locator(MultipleLocator(500))
# ax.legend()
# plt.show()










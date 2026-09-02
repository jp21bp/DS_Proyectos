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
# Importing libraries for portfolio optimization
from pypfopt.efficient_frontier import EfficientFrontier
# from pypfopt import risk_models
# from pypfopt import expected_returns

#################################################
    # Performance Metrics #
##### Function
def performance_metrics(np_port_returns: np.ndarray, periodic_rate: int = 252) -> dict:
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
def fixed_alloc(np_stock_returns: np.ndarray, fixed_weights: np.ndarray) -> np.ndarray:
    # "np_returns".shape = (num_days, num_stocks)
    # "fixed_weights".shape = (num_stocks,)
        # These weights are fixed for the entire portfolio
    # return: np_port_rets, con shape = (num_days)
    assert np_stock_returns.shape[1] == fixed_weights.shape[0]

    np_port_rets = np.matmul(np_stock_returns, fixed_weights.T)
        # In numpy: if "tmp" is 1d vector, then no difference
                # between "tmp" and "tmp.T"
            # Only putting "fixed_weights.T" for notation consistency
        
    return np_port_rets

######################################################
    # Mean-Variance Optimization #
def mvo(np_stock_returns: np.ndarray, window : int = 50) -> np.ndarray:
    # "np_returns".shape = (num_days, num_stocks)
    num_stocks = np_stock_returns.shape[1]
    port_returns = []

    for t in range(window, np_stock_returns.shape[0]):
        # Setup
        window_rets = np_stock_returns[t-window:t]
        win_mean_rets = np.mean(window_rets)
        win_cov_rets = np.cov(window_rets.T)
            # "np.cov": rows = variables/stock, cols = observations
        # MVO
        ef = EfficientFrontier(win_mean_rets, win_cov_rets)
        weights = ef.max_sharpe()
        clean_weights = ef.clean_weights()
        np_port_rets = np.array(list(clean_weights.values()))

        return np_port_rets
    














"""
Performance metrics for the factor momentum strategy.
"""
import pandas as pd
import numpy as np

def annualized_return(returns):
    """Calculate annualized mean return from monthly returns."""
    return returns.mean() * 12

def annualized_volatility(returns):
    """Calculate annualized standard deviation from monthly returns."""
    return returns.std() * np.sqrt(12)

def sharpe_ratio(returns, risk_free_rate=0.0):
    """Calculate annualized Sharpe ratio."""
    excess_returns = returns - (risk_free_rate / 12)
    if excess_returns.std() == 0:
        return 0.0
    return annualized_return(excess_returns) / annualized_volatility(excess_returns)

def max_drawdown(returns):
    """Calculate maximum drawdown from monthly returns."""
    cumulative = (1 + returns).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    return drawdown.min()
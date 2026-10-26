"""
Robustness tests for the FMOM strategy.
"""
import pandas as pd
import os
from fmom import calculate_fmom
from performance import annualized_return, annualized_volatility, sharpe_ratio

def run_robustness():
    print("Running Robustness Tests...\n")
    
    # Load both datasets
    df_us = pd.read_csv('data/processed/us_factors.csv', index_col='Date', parse_dates=True)[['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA']]
    df_cn = pd.read_csv('data/processed/china_factors.csv', index_col='Date', parse_dates=True)[['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA']]

    # --- TEST 1: Transaction Costs (10 bps per trade) ---
    print("--- Test 1: 10 bps Transaction Costs (U.S. 2021-2025) ---")
    df_us_recent = df_us['2021-01-01':]
    
    # We use the same 12-month lookback
    strat_ret, weights = calculate_fmom(df_us_recent, lookback=12)
    
    # Calculate turnover: absolute change in weights from month to month
    turnover = weights.diff().abs().sum(axis=1)
    # Apply cost: 0.10% (0.001) * turnover
    costs = turnover * 0.001 
    
    net_ret = strat_ret - costs
    
    print(f"Gross Sharpe (U.S. 2021-2025): {sharpe_ratio(strat_ret):.2f}")
    print(f"Net Sharpe (after 10 bps costs): {sharpe_ratio(net_ret):.2f}")

    # --- TEST 2: 6-Month Lookback ---
    print("\n--- Test 2: 6-Month Lookback ---")
    # Run the engine with lookback=6 instead of 12
    strat_ret_us_6m, _ = calculate_fmom(df_us, lookback=6)
    strat_ret_cn_6m, _ = calculate_fmom(df_cn, lookback=6)
    
    print(f"U.S. Full Sample Sharpe (6-mo lookback): {sharpe_ratio(strat_ret_us_6m):.2f}")
    print(f"China Sample Sharpe (6-mo lookback): {sharpe_ratio(strat_ret_cn_6m):.2f}")

if __name__ == "__main__":
    run_robustness()
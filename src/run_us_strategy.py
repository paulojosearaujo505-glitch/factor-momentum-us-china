"""
Runs the FMOM strategy on the U.S. Fama-French data.
"""
import pandas as pd
import os
from fmom import calculate_fmom
from performance import annualized_return, annualized_volatility, sharpe_ratio, max_drawdown

def run_us():
    # Load clean U.S. data
    df = pd.read_csv('data/processed/us_factors.csv', index_col='Date', parse_dates=True)
    
    # Ensure we only use the 5 factors (exclude RF)
    factors = ['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA']
    df_factors = df[factors]
    
    # Run FMOM engine
    print("Running FMOM Strategy on U.S. Data...")
    strat_ret, weights = calculate_fmom(df_factors, lookback=12)
    
    # Calculate performance metrics
    ann_ret = annualized_return(strat_ret)
    ann_vol = annualized_volatility(strat_ret)
    sharpe = sharpe_ratio(strat_ret)
    mdd = max_drawdown(strat_ret)
    
    # Print results
    print("\n--- Full U.S. Sample (1963-Present) ---")
    print(f"Annualized Return: {ann_ret*100:.2f}%")
    print(f"Annualized Volatility: {ann_vol*100:.2f}%")
    print(f"Sharpe Ratio: {sharpe:.2f}")
    print(f"Max Drawdown: {mdd*100:.2f}%")
    
    # Save the strategy returns to outputs for later plotting
    os.makedirs('outputs/tables', exist_ok=True)
    strat_ret.to_csv('outputs/tables/us_fmom_returns.csv')
    print("\nStrategy returns saved to outputs/tables/")

if __name__ == "__main__":
    run_us()
"""
Runs the FMOM strategy on the China data.
"""
import pandas as pd
import os
from fmom import calculate_fmom
from performance import annualized_return, annualized_volatility, sharpe_ratio, max_drawdown

def run_china():
    filepath = 'data/processed/china_factors.csv'
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found. Run build_china_panel.py first.")
        return

    # Load clean China data
    df = pd.read_csv(filepath, index_col='Date', parse_dates=True)
    
    # The strategy requires a 12-month lookback. 
    print("Running FMOM Strategy on China Data...")
    strat_ret, weights = calculate_fmom(df, lookback=12)
    
    # Calculate performance metrics
    ann_ret = annualized_return(strat_ret)
    ann_vol = annualized_volatility(strat_ret)
    sharpe = sharpe_ratio(strat_ret)
    mdd = max_drawdown(strat_ret)
    
    print("\n--- China Sample (2021-2025) ---")
    print(f"Annualized Return: {ann_ret*100:.2f}%")
    print(f"Annualized Volatility: {ann_vol*100:.2f}%")
    print(f"Sharpe Ratio: {sharpe:.2f}")
    print(f"Max Drawdown: {mdd*100:.2f}%")
    
    # Save the strategy returns for plotting later
    os.makedirs('outputs/tables', exist_ok=True)
    strat_ret.to_csv('outputs/tables/china_fmom_returns.csv')
    print("\nStrategy returns saved to outputs/tables/")

if __name__ == "__main__":
    run_china()
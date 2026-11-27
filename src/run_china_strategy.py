
"""
Runs the FMOM strategy on the China (CSMAR) factor data.
"""
import os

import pandas as pd

from fmom import calculate_fmom
from performance import annualized_return, annualized_volatility, sharpe_ratio, max_drawdown

FACTORS = ['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA']
SAMPLE_END = '2025-12-31'
LOOKBACK = 12


def report(returns, label):
    """Print the performance metrics for one sample."""
    print(f"\n--- {label}: {returns.index[0]:%Y-%m} to {returns.index[-1]:%Y-%m} "
          f"({len(returns)} months) ---")
    print(f"Annualized Return:     {annualized_return(returns) * 100:.2f}%")
    print(f"Annualized Volatility: {annualized_volatility(returns) * 100:.2f}%")
    print(f"Sharpe Ratio:          {sharpe_ratio(returns):.2f}")
    print(f"Max Drawdown:          {max_drawdown(returns) * 100:.2f}%")


def run_china():
    filepath = 'data/processed/china_factors.csv'
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found. Run build_china_panel.py first.")
        return

    # Load clean China data and keep only the 5 factors
    df = pd.read_csv(filepath, index_col='Date', parse_dates=True)[FACTORS]

    # Run the FMOM engine, then end the sample in December 2025
    print("Running FMOM Strategy on China Data...")
    strat_ret, _ = calculate_fmom(df, lookback=LOOKBACK)
    strat_ret = strat_ret[:SAMPLE_END]

    report(strat_ret, "China Sample")

    # Save the strategy returns for table.py
    os.makedirs('outputs/tables', exist_ok=True)
    strat_ret.to_csv('outputs/tables/china_fmom_returns.csv')
    print("\nStrategy returns saved to outputs/tables/china_fmom_returns.csv")


if __name__ == "__main__":
    run_china()

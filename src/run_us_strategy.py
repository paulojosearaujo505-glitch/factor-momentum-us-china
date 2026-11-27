
"""
Runs the FMOM strategy on the U.S. Fama-French data.
"""
import os

import pandas as pd

from fmom import calculate_fmom
from performance import annualized_return, annualized_volatility, sharpe_ratio, max_drawdown

FACTORS = ['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA']
SAMPLE_END = '2025-12-31'
MATCHED_START = '2022-01-01'
LOOKBACK = 12


def report(returns, label):
    """Print the performance metrics for one sample."""
    print(f"\n--- {label}: {returns.index[0]:%Y-%m} to {returns.index[-1]:%Y-%m} "
          f"({len(returns)} months) ---")
    print(f"Annualized Return:     {annualized_return(returns) * 100:.2f}%")
    print(f"Annualized Volatility: {annualized_volatility(returns) * 100:.2f}%")
    print(f"Sharpe Ratio:          {sharpe_ratio(returns):.2f}")
    print(f"Max Drawdown:          {max_drawdown(returns) * 100:.2f}%")


def run_us():
    filepath = 'data/processed/us_factors.csv'
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found. Run build_panel.py first.")
        return

    # Load clean U.S. data and keep only the 5 factors (exclude RF)
    df = pd.read_csv(filepath, index_col='Date', parse_dates=True)[FACTORS]

    # Run the FMOM engine on the full data, then end the sample in December 2025
    print("Running FMOM Strategy on U.S. Data...")
    strat_ret, _ = calculate_fmom(df, lookback=LOOKBACK)
    strat_ret = strat_ret[:SAMPLE_END]

    # 1. Full sample
    report(strat_ret, "Full U.S. Sample")

    # 2. Matched window (same months as the China strategy)
    report(strat_ret[MATCHED_START:SAMPLE_END], "Matched U.S. Window")

    # Save the strategy returns for table.py
    os.makedirs('outputs/tables', exist_ok=True)
    strat_ret.to_csv('outputs/tables/us_fmom_returns.csv')
    print("\nStrategy returns saved to outputs/tables/us_fmom_returns.csv")


if __name__ == "__main__":
    run_us()


"""
Plots the cumulative return (growth of $1) of the U.S. and China FMOM strategies.

This file is self-contained: it reads the cleaned factor data, runs the
corrected FMOM strategy itself, and saves both charts. It does not depend on
the CSV files written by run_us_strategy.py or run_china_strategy.py.

Run from the project's main folder:
    python src/plot_results.py
"""
import os

import matplotlib
matplotlib.use('Agg')  # save charts to files without needing a screen
import matplotlib.pyplot as plt
import pandas as pd

from fmom import calculate_fmom

FACTORS = ['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA']
SAMPLE_END = '2025-12-31'  # last month used in the paper
LOOKBACK = 12
OUTPUT_DIR = 'outputs/figures'


def load_strategy_returns(data_path):
    """Load cleaned factor data and return monthly FMOM returns up to SAMPLE_END."""
    if not os.path.exists(data_path):
        raise FileNotFoundError(
            f"{data_path} not found. Run the build_*_panel.py scripts first."
        )
    factors = pd.read_csv(data_path, index_col='Date', parse_dates=True)[FACTORS]
    returns, _ = calculate_fmom(factors, lookback=LOOKBACK)
    return returns[:SAMPLE_END]


def plot_growth_of_dollar(returns, market_name, color, output_file):
    """Plot and save the growth of $1 invested in the strategy."""
    cumulative = (1 + returns).cumprod()
    start, end = returns.index[0], returns.index[-1]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(cumulative.index, cumulative, color=color, linewidth=1.5)

    ax.set_title(
        f'{market_name} Factor Momentum Strategy: Growth of $1 ({start:%Y}–{end:%Y})',
        fontsize=14, fontweight='bold'
    )
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Cumulative Growth ($)', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.6)

    # Break-even line at $1.00
    ax.axhline(y=1.0, color='black', linestyle='-', linewidth=1, alpha=0.5)

    plt.tight_layout()
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, output_file)
    plt.savefig(output_path, dpi=300)
    plt.close(fig)

    print(f"{market_name} chart saved to {output_path}")
    print(f"  Covers {start:%Y-%m} to {end:%Y-%m} ({len(returns)} months), "
          f"$1 grows to ${cumulative.iloc[-1]:.2f}\n")


def main():
    us_returns = load_strategy_returns('data/processed/us_factors.csv')
    plot_growth_of_dollar(us_returns, 'U.S.', 'darkblue', 'us_fmom_equity_curve.png')

    china_returns = load_strategy_returns('data/processed/china_factors.csv')
    plot_growth_of_dollar(china_returns, 'China', 'darkred', 'china_fmom_equity_curve.png')


if __name__ == "__main__":
    main()

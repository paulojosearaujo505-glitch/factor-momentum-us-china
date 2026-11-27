
"""
Generates Table 1: Matched Window Performance (January 2022 - December 2025).
"""
import os

import pandas as pd

from performance import annualized_return, annualized_volatility, sharpe_ratio, max_drawdown

US_FILE = 'outputs/tables/us_fmom_returns.csv'
CHINA_FILE = 'outputs/tables/china_fmom_returns.csv'
OUTPUT_FILE = 'outputs/tables/table1_comparison.csv'
SAMPLE_END = '2025-12-31'


def load_returns(path, script_name):
    """Load saved strategy returns as a Series."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} not found. Run {script_name} first.")
    return pd.read_csv(path, index_col=0, parse_dates=True).iloc[:, 0]


def metrics(returns):
    """Return the four Table 1 metrics, formatted for the paper."""
    return [
        f"{annualized_return(returns) * 100:.2f}%",
        f"{annualized_volatility(returns) * 100:.2f}%",
        f"{sharpe_ratio(returns):.2f}",
        f"{max_drawdown(returns) * 100:.2f}%",
    ]


def generate_table_1():
    us_ret = load_returns(US_FILE, 'run_us_strategy.py')
    cn_ret = load_returns(CHINA_FILE, 'run_china_strategy.py')

    # The matched window is the China strategy's trading period
    cn_ret = cn_ret[:SAMPLE_END]
    start, end = cn_ret.index[0], cn_ret.index[-1]
    us_matched = us_ret[start:end]

    if not us_matched.index.equals(cn_ret.index):
        raise ValueError("U.S. and China returns do not cover the same months.")

    table = pd.DataFrame({
        'Metric': ['Annualized Return', 'Annualized Volatility', 'Sharpe Ratio', 'Max Drawdown'],
        'U.S. Matched Sample': metrics(us_matched),
        'China Sample': metrics(cn_ret),
    })

    os.makedirs('outputs/tables', exist_ok=True)
    table.to_csv(OUTPUT_FILE, index=False)

    print(f"\n--- TABLE 1: MATCHED WINDOW PERFORMANCE "
          f"({start:%B %Y} - {end:%B %Y}, {len(cn_ret)} months) ---")
    print(table.to_string(index=False))
    print(f"\nTable saved to {OUTPUT_FILE}\n")


if __name__ == "__main__":
    generate_table_1()

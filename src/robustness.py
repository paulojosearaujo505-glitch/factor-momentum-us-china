"""
Robustness tests for the FMOM strategy
"""
import pandas as pd
from fmom import calculate_fmom
from performance import sharpe_ratio, annualized_return

FACTORS = ['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA']
COST = 0.001  # 10 bps per unit of turnover
START, END = '2022-01-01', '2025-12-31'  # China's trading window


def gross_and_net(df, lookback, start=None, end=None):
    """Run FMOM on the full data, then cut gross and net returns to one window."""
    strat_ret, weights = calculate_fmom(df, lookback=lookback)

    turnover = weights.diff().abs().sum(axis=1)
    first_valid = weights.dropna(how='all').index[0]
    turnover.loc[first_valid] = weights.loc[first_valid].abs().sum()  # opening trade
    costs = turnover * COST

    # Line up on the same months; keep only months where the strategy is invested
    both = pd.concat({'gross': strat_ret, 'cost': costs}, axis=1).dropna()
    both = both[weights.reindex(both.index).abs().sum(axis=1) > 0]
    both['net'] = both['gross'] - both['cost']

    both = both.loc[start:end]
    assert (both['cost'] >= 0).all(), "negative cost found"
    return both


def report(label, both):
    print(f"{label}: {both.index[0]:%Y-%m} to {both.index[-1]:%Y-%m} "
          f"({len(both)} months)")
    print(f"  Gross: return {annualized_return(both['gross']):.2%}, "
          f"Sharpe {sharpe_ratio(both['gross']):.2f}")
    print(f"  Net:   return {annualized_return(both['net']):.2%}, "
          f"Sharpe {sharpe_ratio(both['net']):.2f}")
    print(f"  Avg monthly turnover: {(both['cost'] / COST).mean():.2f}\n")


def run_robustness():
    df_us = pd.read_csv('data/processed/us_factors.csv', index_col='Date',
                        parse_dates=True)[FACTORS]
    df_cn = pd.read_csv('data/processed/china_factors.csv', index_col='Date',
                        parse_dates=True)[FACTORS]

    print("--- Test 1: 10 bps transaction costs (2022-2025) ---")
    report("U.S. matched window", gross_and_net(df_us, 12, START, END))
    report("China", gross_and_net(df_cn, 12, START, END))

    print("--- Test 2: 6-month lookback ---")
    for name, df in [("U.S. full sample", df_us), ("China", df_cn)]:
        for lb in (12, 6):
            both = gross_and_net(df, lb, end=END)
            print(f"{name}, {lb}-month lookback: Sharpe "
                  f"{sharpe_ratio(both['gross']):.2f} "
                  f"({both.index[0]:%Y-%m} to {both.index[-1]:%Y-%m})")


if __name__ == "__main__":
    run_robustness()
"""
Generates Table 1: Matched Window Performance (2021-2025) for the paper.
"""
import pandas as pd
from performance import annualized_return, annualized_volatility, sharpe_ratio, max_drawdown

def generate_table_1():
    # Load strategy returns
    us_ret = pd.read_csv('outputs/tables/us_fmom_returns.csv', index_col=0, parse_dates=True).iloc[:, 0]
    cn_ret = pd.read_csv('outputs/tables/china_fmom_returns.csv', index_col=0, parse_dates=True).iloc[:, 0]

    # Slice the U.S. data to match the China window (2021-01-01 onwards)
    us_ret_matched = us_ret['2021-01-01':]

    # Calculate metrics for both
    metrics = {
        'Metric': ['Annualized Return', 'Annualized Volatility', 'Sharpe Ratio', 'Max Drawdown'],
        'U.S. Matched Sample': [
            f"{annualized_return(us_ret_matched)*100:.2f}%",
            f"{annualized_volatility(us_ret_matched)*100:.2f}%",
            f"{sharpe_ratio(us_ret_matched):.2f}",
            f"{max_drawdown(us_ret_matched)*100:.2f}%"
        ],
        'China Sample': [
            f"{annualized_return(cn_ret)*100:.2f}%",
            f"{annualized_volatility(cn_ret)*100:.2f}%",
            f"{sharpe_ratio(cn_ret):.2f}",
            f"{max_drawdown(cn_ret)*100:.2f}%"
        ]
    }

    # Create DataFrame and save to CSV
    df = pd.DataFrame(metrics)
    df.to_csv('outputs/tables/table1_comparison.csv', index=False)
    
    # Print to terminal so you can copy the exact numbers into your paper
    print("\n--- TABLE 1: MATCHED WINDOW PERFORMANCE (2021-2025) ---")
    print(df.to_string(index=False))
    print("----------------------------------------------------------\n")

if __name__ == "__main__":
    generate_table_1()
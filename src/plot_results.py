"""
Plots the cumulative return (equity curve) of the U.S. and China FMOM strategies.
"""
import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_us_fmom():
    filepath = 'outputs/tables/us_fmom_returns.csv'
    if not os.path.exists(filepath):
        print("Error: Run run_us_strategy.py first to generate the returns.")
        return
        
    df = pd.read_csv(filepath, index_col=0, parse_dates=True)
    returns = df.iloc[:, 0]
    cumulative_returns = (1 + returns).cumprod()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(cumulative_returns.index, cumulative_returns, color='darkblue', linewidth=1.5)
    
    ax.set_title('U.S. Factor Momentum Strategy: Growth of $1 (1963 - Present)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Cumulative Growth', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.axhline(y=1.0, color='black', linestyle='-', linewidth=1, alpha=0.5)
    
    plt.tight_layout()
    output_path = 'outputs/figures/us_fmom_equity_curve.png'
    plt.savefig(output_path, dpi=300)
    print(f"Success! U.S. Figure saved to {output_path}")
    plt.close()

def plot_china_fmom():
    filepath = 'outputs/tables/china_fmom_returns.csv'
    if not os.path.exists(filepath):
        print("Error: Run run_china_strategy.py first to generate the returns.")
        return

    df = pd.read_csv(filepath, index_col=0, parse_dates=True)
    returns = df.iloc[:, 0]
    cumulative_returns = (1 + returns).cumprod()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(cumulative_returns.index, cumulative_returns, color='darkred', linewidth=1.5)
    
    ax.set_title('China Factor Momentum Strategy: Growth of $1 (2022 - 2025)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Cumulative Growth', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.axhline(y=1.0, color='black', linestyle='-', linewidth=1, alpha=0.5)
    
    plt.tight_layout()
    output_path = 'outputs/figures/china_fmom_equity_curve.png'
    plt.savefig(output_path, dpi=300)
    print(f"Success! China Figure saved to {output_path}")
    plt.close()

if __name__ == "__main__":
    plot_us_fmom()
    plot_china_fmom()
"""
Plots the cumulative return (equity curve) of the U.S. FMOM strategy.
"""
import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_us_fmom():
    # Load the strategy returns generated in Session 8
    filepath = 'outputs/tables/us_fmom_returns.csv'
    if not os.path.exists(filepath):
        print("Error: Run run_us_strategy.py first to generate the returns.")
        return
        
    df = pd.read_csv(filepath, index_col=0, parse_dates=True)
    
    # The column name might be unnamed, so we grab the first column
    returns = df.iloc[:, 0]
    
    # Calculate cumulative return (Growth of $1)
    cumulative_returns = (1 + returns).cumprod()
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(cumulative_returns.index, cumulative_returns, color='darkblue', linewidth=1.5)
    
    # Formatting for a professional look
    ax.set_title('U.S. Factor Momentum Strategy: Growth of $1 (1963 - Present)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Cumulative Growth', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.6)
    
    # Add a horizontal line at 1.0 (break-even)
    ax.axhline(y=1.0, color='black', linestyle='-', linewidth=1, alpha=0.5)
    
    plt.tight_layout()
    
    # Save the figure
    os.makedirs('outputs/figures', exist_ok=True)
    output_path = 'outputs/figures/us_fmom_equity_curve.png'
    plt.savefig(output_path, dpi=300)
    print(f"Success! Figure saved to {output_path}")
    
    # Show the plot (if running in an interactive environment)
    plt.show()

if __name__ == "__main__":
    plot_us_fmom()
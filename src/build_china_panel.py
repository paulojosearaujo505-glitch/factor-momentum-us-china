"""
Script to clean the raw CSMAR China factor data.
"""
import pandas as pd
import os

def build_china_panel():
    raw_path = 'data/raw/china_factors_raw.xlsx' 
    
    if not os.path.exists(raw_path):
        print(f"Waiting for data: {raw_path} not found.")
        return

    print(f"Reading raw data from {raw_path}...")
    # The descriptive column names are on the second row (index 1)
    df = pd.read_excel(raw_path, header=1)
    
    # Drop the first row which just says "No Unit"
    df = df.iloc[1:].copy()
    
    # 1. Filter for the All-A-Shares market code (P9709) to avoid duplicates
    df = df[df['Market Type Code'] == 'P9709'].copy()
    
    # 2. Map CSMAR column names to our standard names
    column_mapping = {
        'Trading Month': 'Date',
        'Market Risk Premium Factor (Weighted Average Value of Negotiable Shares)': 'Mkt-RF',
        'Market Value Factor (Weighted Average Value of Negotiable Shares)': 'SMB', 
        'Book-to-Market Ratio Factor (Weighted Average Value of Negotiable Shares)': 'HML',
        'Profitability Factor (Weighted Average Value of Negotiable Shares)': 'RMW',
        'Investment Pattern Factor (Weighted Average Value of Negotiable Shares)': 'CMA'
    }
    df = df.rename(columns=column_mapping)
    
    # 3. Keep only the factors we need
    target_factors = ['Date', 'Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA']
    df = df[target_factors]
    
    # 4. Format the Date column
    df['Date'] = pd.to_datetime(df['Date'])
    
    # 5. CSMAR gives us 3 rows per month (Portfolio Types 1, 2, 3). 
    # We group by Date and take the mean to get a single clean factor return per month.
    df = df.groupby('Date').mean().reset_index()
    df.set_index('Date', inplace=True)
    
    # 6. Save the clean data
    os.makedirs('data/processed', exist_ok=True)
    output_path = 'data/processed/china_factors.csv'
    df.to_csv(output_path)
    
    print(f"Success! Clean data saved to {output_path}")
    print("\nFirst 5 rows of clean China data:")
    print(df.head())

if __name__ == "__main__":
    build_china_panel()
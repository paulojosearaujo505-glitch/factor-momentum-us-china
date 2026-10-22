"""
Script to clean the raw Fama-French data and build the U.S. factor panel.
"""

import pandas as pd
import zipfile
import os

def build_us_panel():
    zip_path = 'data/raw/F-F_Research_Data_5_Factors_2x3_CSV.zip'
    print(f"Reading raw data from {zip_path}...")
    
    # Open the zip file and read the CSV inside it
    with zipfile.ZipFile(zip_path, 'r') as z:
        csv_file = z.namelist()[0]
        with z.open(csv_file) as f:
            # The Fama-French file has 3 lines of metadata before the data
            df = pd.read_csv(f, skiprows=3)
            
    df.columns = ['Date', 'Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA', 'RF']
    
    # Clean the Date column: force to string, strip spaces, and keep only 6-character YYYYMM rows
    df['Date'] = df['Date'].astype(str).str.strip()
    df = df[df['Date'].str.len() == 6].copy()
    
    # Robust date parsing: 'coerce' turns errors into NaT (Not a Time), then we drop them
    df['Date'] = pd.to_datetime(df['Date'], format='%Y%m', errors='coerce')
    df = df.dropna(subset=['Date'])
    df.set_index('Date', inplace=True)
    
    # Convert percentages to decimals (e.g., 1.5% becomes 0.015)
    df = df.astype(float) / 100.0
    
    # Save the clean data
    os.makedirs('data/processed', exist_ok=True)
    output_path = 'data/processed/us_factors.csv'
    df.to_csv(output_path)
    
    print(f"Success! Clean data saved to {output_path}")
    print("\nFirst 5 rows:")
    print(df.head())
    print("\nLast 5 rows:")
    print(df.tail())

if __name__ == "__main__":
    build_us_panel()
"""
Script to download the raw Fama-French 5-Factor dataset.
"""

import requests
import os

def download_ff5():
    url = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_5_Factors_2x3_CSV.zip"
    filepath = 'data/raw/F-F_Research_Data_5_Factors_2x3_CSV.zip'
    
    # Create target directory if it doesn't exist
    os.makedirs('data/raw', exist_ok=True)
    
    # Fetch the ZIP file from the web
    print(f"Downloading data from {url}...")
    response = requests.get(url)
    response.raise_for_status() 
    
    # Save the binary content to the local file
    with open(filepath, 'wb') as f:
        f.write(response.content)
        
    print(f"Success! Raw data saved to {filepath}")

if __name__ == "__main__":
    download_ff5()
"""
Unit tests to verify FMOM engine logic.
"""
import pandas as pd
import numpy as np
from fmom import calculate_fmom 

def test_no_lookahead_bias():
    """Ensure weights are shifted by 1 month to prevent look-ahead bias."""
    # Changed freq='M' to freq='ME' for newer pandas versions
    dates = pd.date_range(start='2020-01-31', periods=24, freq='ME')
    dummy_factors = pd.DataFrame({'Mkt-RF': [0.01]*24, 'SMB': [0.01]*24}, index=dates)
    
    strat_ret, weights = calculate_fmom(dummy_factors, lookback=12)
    
    # The first 12 months have no signal. Month 13 should trade based on month 12.
    assert weights.index[0] == dates[12]
    
def test_weights_sum_to_zero():
    """Ensure the portfolio is dollar-neutral (long sum +1, short sum -1)."""
    # Changed freq='M' to freq='ME' for newer pandas versions
    dates = pd.date_range(start='2020-01-31', periods=24, freq='ME')
    dummy_factors = pd.DataFrame({'Mkt-RF': [0.01]*24, 'SMB': [-0.01]*24}, index=dates)
    
    strat_ret, weights = calculate_fmom(dummy_factors, lookback=12)
    
    assert np.allclose(weights.sum(axis=1), 0.0)
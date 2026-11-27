"""
Core Factor Momentum (FMOM) engine.
"""
import pandas as pd
import numpy as np

def calculate_fmom(factor_returns, lookback=12):
    """Calculate FMOM strategy returns and weights."""
    # 1. Calculate trailing cumulative return over the lookback window
    trailing_ret = (1 + factor_returns).rolling(window=lookback).apply(np.prod, raw=True) - 1

    # 2. Generate signal: 1 for positive, -1 for negative, 0 for zero
    signal = np.sign(trailing_ret)

    # 3. Shift signal by 1 month to avoid look-ahead bias
    # (signal formed at the end of month t, traded in month t+1)
    signal = signal.shift(1)

    # 4. Calculate equal weights
    long_signals = signal.clip(lower=0)
    short_signals = signal.clip(upper=0)

    long_sums = long_signals.sum(axis=1)
    short_sums = short_signals.abs().sum(axis=1)

    # Avoid division by zero if all factors are on one side
    long_sums[long_sums == 0] = 1
    short_sums[short_sums == 0] = 1

    # Scale long side to +1 and short side to -1
    weights = (long_signals.div(long_sums, axis=0)) + (short_signals.div(short_sums, axis=0))

    # 5. Calculate strategy return
    # min_count=1: months with no weights (the lookback warm-up) become NaN, not 0,
    # so they are dropped below together with the empty weights.
    strategy_returns = (weights * factor_returns).sum(axis=1, min_count=1)

    return strategy_returns.dropna(), weights.dropna()
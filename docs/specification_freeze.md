# Methodology and Specification Freeze

**Date:** October 22, 2026
**Project:** Factor Momentum in U.S. and Chinese Equity Markets
**Status:** FROZEN (No changes to these rules will be made after running the data)

## 1. Factor Set
The strategy will utilize the standard Fama-French 5 factors:
1. Market Excess Return (Mkt-RF)
2. Size (SMB)
3. Value (HML)
4. Profitability (RMW)
5. Investment (CMA)

*Note: The RF (risk-free rate) column will be excluded from the momentum rankings, as it is not a traded equity factor.*

## 2. Data Frequency and Horizon
- **Frequency:** Monthly data.
- **U.S. Sample:** Full available history (July 1963 to present) AND a matched 5-year sub-sample (2021–2025) to compare directly with China.
- **China Sample:** 5 consecutive years (2021–2025), based on CSMAR availability.

## 3. Strategy Construction (FMOM)
- **Lookback Period:** 12 months. 
- **Holding Period:** 1 month.
- **Rebalancing:** Monthly, at the end of each month.
- **Signal Generation:** At the end of each month \(t\), calculate the trailing 12-month cumulative return for each of the 5 factors.
- **Portfolio Weights:**
  - Go **LONG** (positive weight) on any factor with a positive trailing 12-month return.
  - Go **SHORT** (negative weight) on any factor with a negative trailing 12-month return.
  - If a factor's trailing return is exactly zero, assign it a weight of zero.
- **Weighting Scheme:** Equal-weighted. If 3 factors have positive returns and 2 have negative, the long side gets a total weight of +1 (each +0.33) and the short side gets a total weight of -1 (each -0.50). *The strategy is dollar-neutral.*

## 4. Performance Metrics
The strategy's return series will be evaluated based on:
- Annualized Mean Return
- Annualized Standard Deviation (Volatility)
- Annualized Sharpe Ratio (assuming a 0% risk-free rate for excess return calculation, as the factors are already in excess terms).
- Maximum Drawdown

## 5. Robustness Tests (Pre-committed)
To ensure the results are not driven by one specific choice, the following tests will be run post-baseline:
- **Lookback Variation:** 6-month lookback instead of 12-month.
- **Weighting Variation:** Value-weighted factor returns instead of equal-weighted (if data permits).
- **Transaction Costs:** Apply a hypothetical 10 basis point (0.10%) cost per trade to the monthly rebalancing.
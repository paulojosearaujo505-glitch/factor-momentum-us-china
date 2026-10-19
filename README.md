# Factor Momentum in U.S. and Chinese Equity Markets

Do factor premia exhibit momentum? I apply an identical long/short factor-timing strategy to six factors in both markets and compare the results.

## Research question
Does a strategy that goes long factors with positive trailing 12-month returns and short factors with negative trailing returns earn significant risk-adjusted returns, and does the effect differ between the U.S. and China?

## Data
- **U.S.**: Kenneth French Data Library, monthly, 1963–2025.
- **China**: [PKU Guanghua / CSMAR — confirm in Session 6], monthly.

## Method
12-month lookback, monthly rebalance, equal-weighted long/short across six factors: Mkt-RF, SMB, HML, RMW, CMA, MOM.

## Key results
*To be added in Session 13.*

## How to reproduce
```bash
pip install -r requirements.txt
python src/download_us.py
python src/download_china.py
python src/build_panel.py
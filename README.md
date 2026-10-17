# Trading Bot
Python based cryptocurrency trading bot project, using Crypto.com price data. #
Does a strategy using MACD and RSI outperform buy-and-hold and random entry baselines on BTC/USD hourly data?

## Data

- Source: Crypto.com from ccxt library, BTC/USD 1hr candles.
- Date range: 2022-01-01 -> 2026-10-1. Earlier data has discontinuities.
- Development range: 2022-01-01 -> 2025-12-31.
- Only closed candles can be used to inform position changes, to avoid bias.

## Method

- `backtest.py` takes prices and position (holding or not) per candle and calculates return and equity at each candle.
- Lookahead bias: A position decided by the closing price of a given candle is held from the open of and receives the return of the **following** candle.
- Fees: a fee is applied to the traded amount whenever the position changes. Taker fees on Crypto.com Exchange are 0.500%.

- `metrics.py` returns the annualised Sharpe ratio, maximum drawdown, trade count, exposure and total return of the strategy.
- The Sharpe ratio of an asset is given by $ \dfrac{R_{p} - R_{f}}{\sigma_{p}} $ where $R_{p}$ is the assets's return, $\sigma_{p}$ is the standard deviation if its return, and $R_{f}$ is the risk free rate, taken to be 0 here.

## Baselines
Results with zero fees:

| strategy | total return | Sharpe | max drawdown | trades | exposure |
|---|---|---|---|---|---|
| buy and hold | +100% | 0.70 | -67% | 1 | 1.00 |
| random entry, 5th percentile | -39% | -0.24 | -70% | 137 | 0.43 |
| random entry, median | +42% | 0.50 | -54% | 157 | 0.50 |
| random entry, 95th percentile | +217% | 1.21 | -33% | 178 | 0.56 |


Random entry: the position flips between 0 and 1 (hold or not) with proability `flip_prob` for each candle. `flip_prob` is set at 0.006, which is approximately 1/168, corresponding to ~1 trade per week. Percentiles are calculated per metric, so a row is not a single run.

Because BTC rose by 100% in the test period, buy and hold's total return is al 100%. Random entry strategies, with exposure of ~50%, also benefited from some of this price rise. Any real strategy must therefore outperform the two baselines to be worthwhile.

## Strategy
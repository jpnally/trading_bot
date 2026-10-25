# Trading Bot

Python-based cryptocurrency trading bot project, using Crypto.com price data.

Does a strategy using MACD and RSI outperform buy-and-hold and random entry baselines on BTC/USD hourly data?

## Data

- Source: Crypto.com from ccxt library, BTC/USD 1hr candles.
- Development range: 2022-01-01 $\rightarrow$ 2025-12-31.
- Test range: 2026-01-01 $\rightarrow$ 2026-10-01.
- Only closed candles can be used to inform position changes, to avoid bias.

## Method

- `backtest.py` takes prices and position (holding or not) per candle and calculates return and equity at each candle.
- Lookahead bias: A position decided by the closing price of a given candle is held from the open of the following candle, and earns that candle's return.
- Fees: a fee is applied to the traded amount whenever the position changes. Taker fees on Crypto.com Exchange (for trade volumes <$10,000) are 0.500%. Maker fees aren't modelled as the available data doesn't show whether a limit order would fill. 
- `metrics.py` returns the annualised Sharpe ratio, maximum drawdown, trade count, exposure and total return of the strategy.
- The Sharpe ratio is

$$ S = \sqrt{N} \frac{\bar{r}}{\sigma_r} $$

where $\bar{r}$ is the mean per-bar return, $\sigma_r$ is the standard deviation of per-bar returns, and $N = 8760$ is the number of hourly bars per year (crypto markets are open 24/7). The risk-free rate is taken to be 0.
- Trade count is the number of position changes, so a closed position counts as 2 trades.

## Baselines

Buy and hold: BTC is bought at the beginning of the development period and held until the end of the period.

Random entry: the position flips between 1 and 0 (hold or not) with probability `flip_prob` for each candle. `flip_prob` is set at 0.006, which is approximately 1/168, corresponding to ~1 trade per week. This was run for 1000 rng seeds. Percentiles are calculated per metric, so a row is not a single run.

### Zero fee:

| strategy | total return | Sharpe | max drawdown | trades | exposure |
|---|---|---|---|---|---|
| buy and hold | +88% | 0.56 | -67% | 1 | 1.00 |
| random entry, 5th percentile | -44% | -0.21 | -70% | 186 | 0.44 |
| random entry, median | +34% | 0.38 | -54% | 209 | 0.50 |
| random entry, 95th percentile | +212% | 0.98 | -35% | 235 | 0.56 |


Because BTC rose by 88% in the development period, buy and hold's total return is also 88%. Random entry strategies, with exposure of ~50%, also benefited from some of this price rise.

### 0.500% fee:

| strategy | total return | Sharpe | max drawdown | trades | exposure |
|---|---|---|---|---|---|
| buy and hold | +87% | 0.56 | -67% | 1 | 1.00 |
| random entry, 5th percentile | -81% | -0.93 | -83% | 186 | 0.44 |
| random entry, median | -53% | -0.32 | -66% | 209 | 0.50 |
| random entry, 95th percentile | +9% | 0.24 | -46% | 235 | 0.56 |

The addition of fees dramatically reduces return and Sharpe ratio. With about 200 trades at 0.500% each, fees reduce final equity to roughly a third of its zero-fee value. Trade frequency therefore matters as much as signal quality.

Each round-trip trade costs 1% in fees, so any real strategy must earn more than 1% per trade to break even.

## Strategy

Not yet run.


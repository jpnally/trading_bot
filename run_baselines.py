import numpy as np
import pandas as pd
from backtest import backtest
from metrics import metrics
from data import fetch_data

coin = "BTC/USD"
timeframe = "1h"
fee = 0
dev_end = "2026-01-01"
flip_prob = 0.006 # ~1 trade per week
num_seeds = 1000

def buy_and_hold(prices):
    position = pd.Series(1, index=prices.index)
    return position

def random_entry(prices, flip_prob, seed):
    rng = np.random.default_rng(seed)
    flips = rng.random(len(prices)) < flip_prob
    position = pd.Series(flips.cumsum() % 2, index=prices.index)
    return position


if __name__ == "__main__":
    
    prices = fetch_data(coin, timeframe).set_index("time")
    prices = prices.loc[prices.index < dev_end]

    print(prices["close"].iloc[-1] / prices["close"].iloc[0] - 1)
    
    random_entry_rows = {}

    for seed in range(num_seeds):
        random_entry_rows[seed] = metrics(backtest(prices, random_entry(prices, flip_prob, seed), fee))

    random_entry_df = pd.DataFrame(random_entry_rows)
    random_entry_df.T.to_csv("results/random_entry.csv", index_label="seed")

    q = random_entry_df.T.quantile([0.05, 0.5, 0.95])

    rows = {}
    rows["buy_and_hold"] = metrics(backtest(prices, buy_and_hold(prices), fee))
    rows["random_p05"] = q.loc[0.05].to_dict()
    rows["random_p50"] = q.loc[0.5].to_dict()
    rows["random_p95"] = q.loc[0.95].to_dict()
    pd.DataFrame(rows).T.round(3).to_csv(f"re. i've sults/summary_fee{fee}.csv", index_label="strategy")

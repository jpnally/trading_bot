import numpy as np
import pandas as pd

def backtest(prices, position, fee):
    bar_ret = prices["close"].pct_change().fillna(0)

    held = position.shift(1).fillna(0)

    gross = bar_ret * held
    cost = fee * held.diff().abs().fillna(0)

    net = gross - cost
    equity = (1 + net).cumprod()

    return pd.DataFrame({
        "bar_ret": bar_ret,
        "held": held,
        "cost": cost,
        "gross": gross,
        "net": net,
        "equity": equity,
    })

if __name__ == "__main__":
    prices = pd.read_csv("price_data/BTC_USD_1h.csv", parse_dates=["time"]).set_index("time")
    fee = 0.005
    position = pd.Series(1, index=prices.index)

    backtest(prices, position, fee).to_csv("results/equity/buy_hold.csv")





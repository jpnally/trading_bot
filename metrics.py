import numpy as np
import pandas as pd
from backtest import backtest

def metrics(result, periods_in_year = 24*365):
    net = result["net"]
    equity = result["equity"]
    held = result["held"]
    
    sharpe_ratio = np.sqrt(periods_in_year) * net.mean() / net.std() if net.sum() != 0 else "N/A"

    peak_equity = equity.cummax()
    max_drawdown = (equity/peak_equity - 1).min()

    trade_count = held.diff().abs().sum()

    exposure = held.mean()

    total_return = equity[-1] - 1

    return {
        "sharpe_ratio": float(sharpe_ratio),
        "max_drawdown": float(max_drawdown),
        "trade_count": int(trade_count),
        "exposure": float(exposure),
        "return": float(total_return)
        }

if __name__ == "__main__":

    result = pd.read_csv("results/equity/buy_hold.csv")
    print(metrics(result))
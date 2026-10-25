import pandas as pd

def macd(close: pd.Series, fast=12, slow=26, signal=9):
    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()

    macd_line = ema_fast - ema_slow

    signal_line = macd_line.ewm(span=signal, adjust=False).mean()

    hist = macd_line - signal_line

    return pd.DataFrame({
        "macd": macd_line,
        "signal": signal_line,
        "hist": hist,
    })

def rsi(close: pd.Series, period=14):

    change = close.diff()

    up = change.clip(lower=0)
    down = change.clip(upper=0).abs()

    up_avg = up.ewm(alpha=1/period, adjust=False).mean()
    down_avg = down.ewm(alpha=1/period, adjust=False).mean()

    rs =  up_avg / down_avg
    rsi = 100 - 100/(1 + rs)

    return rsi


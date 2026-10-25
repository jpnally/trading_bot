import pandas as pd
import numpy as np
from indicators import macd, rsi

def test_constant_price():
    prices = pd.Series([100.0] * 50)

    # when the price is constant, the moving average is constant for any period, fast - slow = 0
    assert np.allclose(macd(prices), 0)

    # average gain and average loss are 0, so rsi calculation contains 0/0=NaN
    assert np.isnan(rsi(prices)).all()


def test_rising_price():
    prices = pd.Series(range(1, 60), dtype=float)

    macd_res = macd(prices)
    rsi_res = rsi(prices).dropna() # first value is NaN
    
    # the fast ema is closer to the current price than slow
    # when the price is constantly rising, fast - slow should be positive
    assert (macd_res["macd"].iloc[1:] > 0).all()

    # down_avg is 0, so rs is infinite and rsi is 100
    assert (np.allclose(rsi_res, 100))


# fast=1 makes fast equal the current price
# slow=3 gives alpha = 2/(3+1) = 0.5
# signal=4 gives alpha = 0.4
# expect macd [0, 5, -7.5], signal [0, 2, -1.8], hist [0, 3, -5.7]
def test_macd_hand_calc():
    prices = pd.Series([100, 110, 90], dtype=float)

    result = macd(prices, fast=1, slow=3, signal=4)

    assert np.isclose(result["macd"], [0, 5, -7.5]).all()
    assert np.isclose(result["signal"], [0, 2, -1.8]).all()
    assert np.isclose(result["hist"], [0, 3, -5.7]).all()
    

import numpy as np
import pandas as pd
from backtest import backtest

def test_long_position():
    close = pd.Series([50, 55, 52, 60, 58], index = np.arange(5))
    prices = pd.DataFrame({
        "close": close
    })
    position = pd.Series(1, index=prices.index)

    result = backtest(prices, position, fee=0)
    
    # when constantly holding, final value of equity should be equal to end price/start price
    assert np.isclose(result["equity"].iloc[-1], close.iloc[-1]/close.iloc[0])

def test_position_lagged_one_candle():
    close = pd.Series([110, 105, 100, 50, 70], index = np.arange(5))
    prices = pd.DataFrame({
            "close": close
    })
    position = pd.Series([0, 0, 1, 0, 0], index=prices.index)

    result = backtest(prices, position, fee = 0)

    # demonstrates the shift by 1 in position in backtest function
    # buy signal established at end of candle 3, hold during candle 4, which had -50% return
    assert np.isclose(result["equity"].iloc[-1], 0.5)

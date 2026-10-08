import ccxt
import pandas as pd
import os
import logging
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()
exchange = ccxt.cryptocom({
    'apiKey':          os.getenv('apiKey'),
    'secret':          os.getenv('secretKey'),
    'enableRateLimit': True,
})

# save price data to csv file or fetch from cached data
# crypto.com allows 300 candles per request
def fetch_data(coin, timeframe):
    filename = f"price_data/{coin.replace("/","_")}_{timeframe}.csv"

    if os.path.exists(filename):
        df = pd.read_csv(filename, parse_dates=["time"])
        logger.info("Loaded cached %s %s data.", timeframe, coin)
        return df

    since = datetime(2022,1,1,0,0,0, tzinfo=timezone.utc)
    since = int(since.timestamp()*1000)

    end = datetime(2026,1,1,0,0,0, tzinfo=timezone.utc)
    end = int(end.timestamp()*1000)

    all_candles = []

    request = 0
    while True:
        candles = exchange.fetch_ohlcv(coin, timeframe=timeframe, since=since, limit=300)
        request += 1
        if not candles:
            logger.warning("request %d: EMPTY, since=%s", request, exchange.iso8601(since))
            break
        logger.debug("request %d: %d candles, %s - %s", request, len(candles),
            exchange.iso8601(candles[0][0]), exchange.iso8601(candles[-1][0]))
        
        all_candles += candles
        since = candles[-1][0] + 1
        if candles[-1][0] > end:
            break

    df = pd.DataFrame(all_candles, columns=["time", "open", "high", "low", "close", "vol"])
    df["time"] = pd.to_datetime(df["time"], unit = "ms")
    df.to_csv(filename, index=False)
    logger.info("Saved %s %s data.", timeframe, coin)
    return df

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    fetch_data("BTC/USD", "1h")




    




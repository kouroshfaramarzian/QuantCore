from MetaTrader5 import TIMEFRAME_M1

from src.data.pipeline import DataPipeline
from src.data.providers.mt5_provider import MT5Provider
from src.features.indicators import Indicators

provider = MT5Provider()

pipeline = DataPipeline(provider)

df = pipeline.run(
    symbol="XAUUSD",
    timeframe=TIMEFRAME_M1,
)

df["EMA20"] = Indicators.ema(df, 20)
df["EMA50"] = Indicators.ema(df, 50)
df["EMA200"] = Indicators.ema(df, 200)

print(df.tail())
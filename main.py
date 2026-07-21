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
df["RSI14"] = Indicators.rsi(df)
df["ATR14"] = Indicators.atr(df)
macd, signal, hist = Indicators.macd(df)

df["MACD"] = macd
df["MACD_SIGNAL"] = signal
df["MACD_HIST"] = hist
print(df.tail())
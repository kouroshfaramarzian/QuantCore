from MetaTrader5 import TIMEFRAME_M1

from src.data.pipeline import DataPipeline
from src.data.providers.mt5_provider import MT5Provider
from src.features.feature_engine import FeatureEngine
from src.strategy.signal_engine import SignalEngine


provider = MT5Provider()

pipeline = DataPipeline(provider)

df = pipeline.run(
    symbol="XAUUSD",
    timeframe=TIMEFRAME_M1,
)

df = FeatureEngine.transform(df)

signal = SignalEngine.generate(df)

print("=" * 40)
print("QuantCore Signal")
print("=" * 40)
print(signal)
print("=" * 40)
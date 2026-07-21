from MetaTrader5 import TIMEFRAME_M1

from src.data.pipeline import DataPipeline
from src.data.providers.mt5_provider import MT5Provider
from src.features.feature_engine import FeatureEngine


provider = MT5Provider()

pipeline = DataPipeline(provider)

df = pipeline.run(
    symbol="XAUUSD",
    timeframe=TIMEFRAME_M1,
)

df = FeatureEngine.transform(df)

print(df.tail())
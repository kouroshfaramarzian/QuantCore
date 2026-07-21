from MetaTrader5 import TIMEFRAME_M1

from src.data.data_manager import DataManager
from src.data.pipeline import DataPipeline
from src.data.providers.mt5_provider import MT5Provider

provider = MT5Provider()

pipeline = DataPipeline(provider)

df = pipeline.run(
    symbol="XAUUSD",
    timeframe=TIMEFRAME_M1,
)

manager = DataManager()

path = manager.save(
    df,
    symbol="XAUUSD",
    timeframe="M1",
)

print(path)
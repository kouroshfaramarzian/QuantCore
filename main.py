from MetaTrader5 import TIMEFRAME_M1

from src.data.pipeline import DataPipeline
from src.data.providers.mt5_provider import MT5Provider

from src.features.feature_engine import FeatureEngine

from src.strategy.signal_engine import SignalEngine

from src.risk.risk_engine import RiskEngine


provider = MT5Provider()

pipeline = DataPipeline(provider)

df = pipeline.run(
    symbol="XAUUSD",
    timeframe=TIMEFRAME_M1,
)

df = FeatureEngine.transform(df)

result = SignalEngine.generate(df)

trade = RiskEngine.calculate(
    df,
    result["signal"].value,
)

print("=" * 60)
print("                QuantCore")
print("=" * 60)

print(f"Signal       : {result['signal'].value}")
print(f"BUY Score    : {result['buy_score']}")
print(f"SELL Score   : {result['sell_score']}")

print("-" * 60)

print(f"Entry        : {trade['entry']}")
print(f"Stop Loss    : {trade['stop_loss']}")
print(f"Take Profit  : {trade['take_profit']}")

print("=" * 60)

provider.disconnect()
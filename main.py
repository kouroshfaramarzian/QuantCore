from MetaTrader5 import TIMEFRAME_M1

from src.data.pipeline import DataPipeline
from src.data.providers.mt5_provider import MT5Provider

from src.features.feature_engine import FeatureEngine

from src.strategy.signal_engine import SignalEngine

from src.risk.risk_engine import RiskEngine

from src.backtest.backtester import Backtester
from src.backtest.statistics import Statistics
from src.backtest.report import Report


def main():

    # -----------------------------
    # Provider
    # -----------------------------

    provider = MT5Provider()

    try:

        # -----------------------------
        # Data Pipeline
        # -----------------------------

        pipeline = DataPipeline(provider)

        df = pipeline.run(
            symbol="XAUUSD",
            timeframe=TIMEFRAME_M1,
        )

        # -----------------------------
        # Feature Engineering
        # -----------------------------

        df = FeatureEngine.transform(df)

        # -----------------------------
        # Strategy
        # -----------------------------

        signal = SignalEngine.generate(df)

        # -----------------------------
        # Risk Management
        # -----------------------------

        risk = RiskEngine.calculate(
            df,
            signal["signal"].value,
        )

        # -----------------------------
        # Backtest
        # -----------------------------

        backtester = Backtester()

        trades = backtester.run(df)

        # -----------------------------
        # Statistics
        # -----------------------------

        stats = Statistics.calculate(trades)

        # -----------------------------
        # Live Signal
        # -----------------------------

        print("=" * 60)
        print("                  QuantCore")
        print("=" * 60)

        print(f"Signal       : {signal['signal'].value}")
        print(f"BUY Score    : {signal['buy_score']}")
        print(f"SELL Score   : {signal['sell_score']}")

        print("-" * 60)

        print(f"Entry        : {risk['entry']}")
        print(f"Stop Loss    : {risk['stop_loss']}")
        print(f"Take Profit  : {risk['take_profit']}")

        print("=" * 60)

        # -----------------------------
        # Backtest Report
        # -----------------------------

        Report.show(stats)

        # -----------------------------
        # Debug (Optional)
        # -----------------------------

        # for trade in trades:
        #     print(trade)

    finally:

        provider.disconnect()


if __name__ == "__main__":

    main()

from datetime import datetime

from src.execution.order import Order
from src.execution.order_manager import OrderManager


order = Order(

    symbol="XAUUSD",

    direction="BUY",

    volume=1.0,

    entry_price=2400,

    stop_loss=2395,

    take_profit=2410,

    open_time=datetime.now(),

)

position = OrderManager.execute(order)

print(position)
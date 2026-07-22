from datetime import datetime

from MetaTrader5 import TIMEFRAME_M1

from src.data.pipeline import DataPipeline
from src.data.providers.mt5_provider import MT5Provider

from src.features.feature_engine import FeatureEngine

from src.context.context_engine import ContextEngine

from src.strategy.signal_engine import SignalEngine

from src.risk.risk_engine import RiskEngine

from src.backtest.backtester import Backtester
from src.backtest.statistics import Statistics
from src.backtest.report import Report

from src.evaluation.splitter import DataSplitter
from src.evaluation.walk_forward import WalkForwardValidator

from src.execution.order import Order
from src.execution.order_manager import OrderManager


def main():

    provider = MT5Provider()

    try:

        # ==========================================
        # DATA
        # ==========================================

        pipeline = DataPipeline(provider)

        df = pipeline.run(

            symbol="XAUUSD",

            timeframe=TIMEFRAME_M1,

        )

        # ==========================================
        # FEATURES
        # ==========================================

        df = FeatureEngine.transform(df)

        # ==========================================
        # DATASET SPLIT
        # ==========================================

        train_df, validation_df, test_df = (

            DataSplitter.split(df)

        )

        print()

        print("=" * 60)
        print("Dataset")
        print("=" * 60)

        print(f"Train      : {len(train_df)}")
        print(f"Validation : {len(validation_df)}")
        print(f"Test       : {len(test_df)}")

        # ==========================================
        # MARKET CONTEXT
        # ==========================================

        context = ContextEngine.build(test_df)

        print()

        print("=" * 60)
        print("Market Context")
        print("=" * 60)

        print(context)

        # ==========================================
        # SIGNAL
        # ==========================================

        test_df = SignalEngine.generate_series(test_df)

        signal = SignalEngine.generate(test_df)

        print()

        print("=" * 60)
        print("Strategy Debug")
        print("=" * 60)

        last = test_df.iloc[-1]

        print(f"EMA20        : {last['EMA20']:.2f}")
        print(f"EMA50        : {last['EMA50']:.2f}")
        print(f"EMA200       : {last['EMA200']:.2f}")

        print("-" * 60)

        print(f"MACD         : {last['MACD']:.4f}")
        print(f"MACD SIGNAL  : {last['MACD_SIGNAL']:.4f}")

        print("-" * 60)

        print(f"RSI14        : {last['RSI14']:.2f}")

        print("-" * 60)

        print(f"IS_BULLISH   : {last['IS_BULLISH']}")
        print(f"IS_BEARISH   : {last['IS_BEARISH']}")

        print("-" * 60)

        print(f"BUY SCORE    : {signal['buy_score']}")
        print(f"SELL SCORE   : {signal['sell_score']}")

        print("=" * 60)
        # ==========================================
        # RISK
        # ==========================================

        risk = RiskEngine.calculate(

            test_df,

            signal["signal"].value,

        )

        # ==========================================
        # BACKTEST
        # ==========================================

        backtester = Backtester()

        trades = backtester.run(test_df)

        statistics = Statistics()

        for trade in trades:
            statistics.update(trade)

        stats = statistics.summary()
        
        # ==========================================
        # LIVE SIGNAL
        # ==========================================

        print()

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

        # ==========================================
        # BACKTEST REPORT
        # ==========================================

        Report.show(stats)

        # ==========================================
        # WALK FORWARD
        # ==========================================

        print()

        print("=" * 60)
        print("Walk Forward Validation")
        print("=" * 60)

        results = WalkForwardValidator.run(train_df)

        for i, result in enumerate(results, start=1):

            print()

            print(f"Window {i}")

            print(result)

        # ==========================================
        # EXECUTION TEST
        # ==========================================

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

        print()

        print("=" * 60)
        print("Execution Test")
        print("=" * 60)

        print(position)

    finally:

        provider.disconnect()


if __name__ == "__main__":

    main()
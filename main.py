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
from src.market.swing import SwingDetector
from src.market.bos import BOSDetector
from src.market.choch import CHOCHDetector
from src.context.market_state import MarketStateResolver
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
        df = SwingDetector.detect(df)
        df = BOSDetector.detect(df)
        df = CHOCHDetector.detect(df)
        train_df, validation_df, test_df = DataSplitter.split(df)

        print("\n============== BOS ==============\n")

        print(
            test_df[
                [
                    "close",
                    "SWING_HIGH",
                    "SWING_LOW",
                    "BULLISH_BOS",
                    "BEARISH_BOS",
                ]
            ].tail(40)
        )

        print("\n===============================\n")

        print("\n============== CHOCH ==============\n")

        print(
            test_df[
                [
                    "close",
                    "STRUCTURE",
                    "CHOCH_BULLISH",
                    "CHOCH_BEARISH",
                ]
            ].tail(50)
        )

        print("\n===================================\n")
        # ==========================================
        # DATASET SPLIT
        # ==========================================

        train_df, validation_df, test_df = (

            DataSplitter.split(df)

        )
        test_df = SwingDetector.detect(test_df)
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
        last_row = test_df.iloc[-1]

        market_state = MarketStateResolver.resolve(last_row)

        print()
        print("=" * 60)
        print("Market State")
        print("=" * 60)

        print(f"STATE : {market_state}")

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

        print(f"Trend        : {signal['trend']}")
        print(f"Trigger      : {signal['trigger']}")
        

        print("=" * 60)
        # ==========================================
        # RISK
        # ==========================================

        risk = RiskEngine.calculate(

            test_df,

            signal["signal"],

        )

        # ==========================================
        # BACKTEST
        # ==========================================

        backtester = Backtester()

        trades = backtester.run(test_df)

        statistics = Statistics()

        for trade in trades:
            statistics.update(trade)

        stats = statistics.summary(backtester.engine.portfolio)
        
                # ==========================================
        # LIVE SIGNAL
        # ==========================================

        print()

        print("=" * 60)
        print("                  QuantCore")
        print("=" * 60)

        print(f"Signal       : {signal['signal']}")
        print(f"Trend        : {signal['trend']}")
        print(f"Trigger      : {signal['trigger']}")

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
from __future__ import annotations

from datetime import datetime

from MetaTrader5 import TIMEFRAME_M1


from src.data.pipeline import DataPipeline
from src.data.providers.mt5_provider import MT5Provider

from src.features.feature_engine import FeatureEngine


from src.market.swing import SwingDetector
from src.market.bos import BOSDetector
from src.market.choch import CHOCHDetector
from src.market.structure_engine import StructureEngine


from src.context.context_engine import ContextEngine
from src.context.market_state import MarketStateResolver


from src.strategy.signal_engine import SignalEngine
from src.strategy.decision_engine import DecisionEngine


from src.risk.risk_engine import RiskEngine


from src.backtest.backtester import Backtester
from src.backtest.report import Report
from src.backtest.statistics import Statistics


from src.evaluation.splitter import DataSplitter
from src.evaluation.walk_forward import WalkForwardValidator


from src.execution.order import Order
from src.execution.order_manager import OrderManager



def main():

    provider = MT5Provider()


    try:

        print("=" * 60)
        print("QuantCore START")
        print("=" * 60)



        # ==========================================
        # DATA
        # ==========================================

        pipeline = DataPipeline(provider)


        df = pipeline.run(

            symbol="XAUUSD",

            timeframe=TIMEFRAME_M1,

        )


        if df is None or df.empty:

            raise Exception(
                "No market data received"
            )



        # ==========================================
        # FEATURES
        # ==========================================

        df = FeatureEngine.transform(df)



        # ==========================================
        # MARKET STRUCTURE PIPELINE
        # ==========================================


        # 1 - Swing

        df = SwingDetector.detect(df)



        # 2 - BOS

        df = BOSDetector.detect(df)



        print()

        print("BOS DISTRIBUTION")

        print(
            df[
                [
                    "BULLISH_BOS",
                    "BEARISH_BOS"
                ]
            ].sum()
        )



        # 3 - Initial Structure

        df = StructureEngine.build(df)



        # 4 - CHOCH

        df = CHOCHDetector.detect(df)



        # 5 - Final Structure update

        df = StructureEngine.build(df)



        print()

        print("CHOCH DISTRIBUTION")

        print(
            df[
                [
                    "CHOCH_BULLISH",
                    "CHOCH_BEARISH"
                ]
            ].sum()
        )



        print()

        print("STRUCTURE DISTRIBUTION")

        print(
            df["STRUCTURE"]
            .value_counts()
        )




        # ==========================================
        # SPLIT
        # ==========================================


        train_df, validation_df, test_df = DataSplitter.split(df)



        if test_df.empty:

            raise Exception(
                "Empty test dataframe"
            )



        # ==========================================
        # STRUCTURE DEBUG
        # ==========================================


        last = test_df.iloc[-1]


        print()

        print("STRUCTURE DEBUG")


        print(
            last[
                [
                    "STRUCTURE",
                    "STRUCTURE_SCORE",
                    "STRUCTURE_REASON",
                    "EMA20",
                    "EMA50",
                    "EMA200",
                    "BULLISH_BOS",
                    "BEARISH_BOS",
                    "CHOCH_BULLISH",
                    "CHOCH_BEARISH",
                ]
            ]
        )



        # ==========================================
        # CONTEXT
        # ==========================================


        context = ContextEngine.build(test_df)


        print()

        print("MARKET CONTEXT")

        print(context)




        # ==========================================
        # MARKET STATE
        # ==========================================


        market_state = MarketStateResolver.resolve(last)


        print()

        print("MARKET STATE")

        print(market_state)




        # ==========================================
        # SIGNAL
        # ==========================================


        test_df = SignalEngine.generate_series(
            test_df
        )


        signal = SignalEngine.generate(
            test_df
        )


        print()

        print("SIGNAL DISTRIBUTION")

        print(
            test_df["signal"]
            .value_counts()
        )



        print()

        print("LIVE SIGNAL")

        print(signal)




        # ==========================================
        # DECISION
        # ==========================================


        decision = DecisionEngine.decide(


            structure=last.get(
                "STRUCTURE",
                "RANGE"
            ),


            bullish_bos=bool(
                last.get(
                    "BULLISH_BOS",
                    False
                )
            ),


            bearish_bos=bool(
                last.get(
                    "BEARISH_BOS",
                    False
                )
            ),


            choch_bullish=bool(
                last.get(
                    "CHOCH_BULLISH",
                    False
                )
            ),


            choch_bearish=bool(
                last.get(
                    "CHOCH_BEARISH",
                    False
                )
            ),


            trigger=signal.get(
                "trigger",
                "HOLD"
            ),


            confidence=signal.get(
                "confidence",
                0
            ),


        )


        print()

        print("DECISION")

        print(decision)




        # ==========================================
        # RISK
        # ==========================================


        risk = RiskEngine.calculate(

            test_df,

            signal.get(
                "signal",
                "HOLD"
            )

        )


        print()

        print("RISK")

        print(risk)




        # ==========================================
        # BACKTEST
        # ==========================================


        backtester = Backtester()


        trades = backtester.run(
            test_df
        )


        statistics = Statistics()


        for trade in trades:

            statistics.update(trade)



        stats = statistics.summary(
            backtester.engine.portfolio
        )



        print()

        Report.show(stats)




        # ==========================================
        # WALK FORWARD
        # ==========================================


        print()

        print("Walk Forward")


        results = WalkForwardValidator.run(
            train_df
        )


        for r in results:

            print(r)




        # ==========================================
        # EXECUTION
        # ==========================================


        if risk["entry"] is not None:


            order = Order(

                symbol="XAUUSD",

                direction=signal["signal"],

                volume=1.0,

                entry_price=risk["entry"],

                stop_loss=risk["stop_loss"],

                take_profit=risk["take_profit"],

                open_time=datetime.now(),

            )



            position = OrderManager.execute(
                order
            )


            print()

            print("EXECUTION")

            print(position)



        else:


            print()

            print(
                "Execution skipped - no valid risk"
            )



    finally:

        provider.disconnect()




if __name__ == "__main__":

    main()
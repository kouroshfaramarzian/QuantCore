from datetime import datetime

from MetaTrader5 import TIMEFRAME_M1


from src.data.pipeline import DataPipeline
from src.data.providers.mt5_provider import MT5Provider


from src.features.feature_engine import FeatureEngine


from src.context.context_engine import ContextEngine
from src.context.market_state import MarketStateResolver


from src.market.swing import SwingDetector
from src.market.bos import BOSDetector
from src.market.choch import CHOCHDetector
from src.market.structure_engine import StructureEngine


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


        pipeline = DataPipeline(
            provider
        )


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


        df = FeatureEngine.transform(
            df
        )



        # ==========================================
        # MARKET STRUCTURE
        # ==========================================


        df = SwingDetector.detect(
            df
        )


        df = BOSDetector.detect(
            df
        )


        df = CHOCHDetector.detect(
            df
        )


        print()

        print("BOS BEFORE STRUCTURE")


        print(

            df[
                [
                    "BULLISH_BOS",
                    "BEARISH_BOS"
                ]
            ]
            .sum()

        )



        df = StructureEngine.build(
            df
        )



        print()


        print(
            df[
                [
                    "STRUCTURE",
                    "STRUCTURE_SCORE",
                    "STRUCTURE_REASON",
                    "BULLISH_BOS",
                    "BEARISH_BOS",
                    "CHOCH_BULLISH",
                    "CHOCH_BEARISH",
                ]
            ]
            .tail(10)
        )



        print()

        print("BOS DISTRIBUTION")


        print(

            df[
                [
                    "BULLISH_BOS",
                    "BEARISH_BOS"
                ]
            ]
            .sum()

        )



        print()

        print("CHOCH DISTRIBUTION")


        print(

            df[
                [
                    "CHOCH_BULLISH",
                    "CHOCH_BEARISH"
                ]
            ]
            .sum()

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


        train_df, validation_df, test_df = DataSplitter.split(
            df
        )



        if test_df.empty:

            raise Exception(
                "Empty test dataframe"
            )



        # ==========================================
        # SIGNAL GENERATION
        # ==========================================


        test_df = SignalEngine.generate_series(
            test_df
        )



        decisions = []



        for _, row in test_df.iterrows():


            decision = DecisionEngine.decide(

                signal=row.get(
                    "signal",
                    "HOLD"
                ),


                confidence=int(
                    row.get(
                        "confidence",
                        0
                    )
                ),


                trend=row.get(
                    "trend",
                    "RANGE"
                ),


                reason=row.get(
                    "reason",
                    ""
                ),

            )


            decisions.append(

                decision["signal"]

            )



        test_df["decision"] = decisions
                # ==========================================
        # DEBUG
        # ==========================================


        print()

        print("STRUCTURE DEBUG")


        print(

            test_df[

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

            .tail(1)

            .T

        )



        last = test_df.iloc[-1]



        # ==========================================
        # CONTEXT
        # ==========================================


        context = ContextEngine.build(

            test_df

        )


        print()

        print("MARKET CONTEXT")

        print(context)



        # ==========================================
        # MARKET STATE
        # ==========================================


        market_state = MarketStateResolver.resolve(

            last

        )


        print()

        print("MARKET STATE")

        print(market_state)



        # ==========================================
        # LIVE SIGNAL
        # ==========================================


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
        # LIVE DECISION
        # ==========================================


        decision = DecisionEngine.decide(

            signal=signal.get(

                "signal",

                "HOLD"

            ),


            confidence=int(

                signal.get(

                    "confidence",

                    0

                )

            ),


            trend=signal.get(

                "trend",

                "RANGE"

            ),


            reason=signal.get(

                "reason",

                ""

            )

        )



        print()

        print("DECISION")

        print(decision)



        # ==========================================
        # RISK
        # ==========================================


        risk = RiskEngine.calculate(

            test_df,

            decision.get(

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


            statistics.update(

                trade

            )



        stats = statistics.summary(

            backtester.engine.portfolio

        )



        print()

        Report.show(

            stats

        )



        # ==========================================
        # WALK FORWARD
        # ==========================================


        print()

        print("Walk Forward")



        results = WalkForwardValidator.run(

            train_df

        )



        for result in results:


            print(result)



        # ==========================================
        # EXECUTION
        # ==========================================


        if risk.get(

            "entry"

        ) is not None:



            order = Order(

                symbol="XAUUSD",


                direction=decision.get(

                    "signal",

                    "HOLD"

                ),


                volume=1.0,


                entry_price=risk.get(

                    "entry"

                ),


                stop_loss=risk.get(

                    "stop_loss"

                ),


                take_profit=risk.get(

                    "take_profit"

                ),


                open_time=datetime.now()

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
# main.py

from MetaTrader5 import TIMEFRAME_M1


from src.data.providers.mt5_provider import MT5Provider
from src.data.pipeline import DataPipeline


from src.features.feature_engine import FeatureEngine


from src.market.swing import SwingDetector
from src.market.bos import BOSDetector
from src.market.choch import CHOCHDetector
from src.market.structure_engine import StructureEngine


from src.strategy.signal_engine import SignalEngine
from src.strategy.decision_engine import DecisionEngine


from src.risk.risk_engine import RiskEngine


from src.backtest.backtester import Backtester


from src.evaluation.splitter import DataSplitter
from src.evaluation.walk_forward import WalkForwardValidator





def main():


    provider = MT5Provider()



    try:


        print("=" * 60)

        print(
            "QuantCore START"
        )

        print("=" * 60)





        # =====================================
        # DATA
        # =====================================


        pipeline = DataPipeline(

            provider

        )



        df = pipeline.run(

            symbol="XAUUSD",

            timeframe=TIMEFRAME_M1

        )



        if df is None or df.empty:

            raise Exception(
                "No market data"
            )





        # =====================================
        # FEATURES
        # =====================================


        df = FeatureEngine.transform(

            df

        )





        # =====================================
        # MARKET STRUCTURE
        # =====================================


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


        print(
            "BOS BEFORE STRUCTURE"
        )


        print(

            df[

                [
                    "BULLISH_BOS",
                    "BEARISH_BOS"
                ]

            ].sum()

        )




        df = StructureEngine.build(

            df

        )



        print()


        print(
            "STRUCTURE DISTRIBUTION"
        )


        print(

            df["STRUCTURE"]

            .value_counts()

        )






        # =====================================
        # SPLIT DATA
        # =====================================


        train_df, validation_df, test_df = DataSplitter.split(

            df

        )



        if test_df.empty:


            raise Exception(
                "Empty test data"
            )





        # =====================================
        # SIGNAL GENERATION
        # =====================================


        test_df = SignalEngine.generate_series(

            test_df

        )




        print()


        print(
            "SIGNAL DISTRIBUTION"
        )



        print(

            test_df["signal"]

            .value_counts()

        )






        # =====================================
        # LIVE SIGNAL
        # =====================================


        live_signal = SignalEngine.generate(

            df

        )



        print()


        print(
            "LIVE SIGNAL"
        )


        print(

            live_signal

        )




        decision = DecisionEngine.decide(

            signal=live_signal.get(
                "signal",
                "HOLD"
            ),


            confidence=live_signal.get(
                "confidence",
                0
            ),


            trend=live_signal.get(
                "trend",
                "RANGE"
            ),


            reason=live_signal.get(
                "reason",
                ""
            )

        )




        print()


        print(
            "DECISION"
        )


        print(

            decision

        )







        # =====================================
        # RISK DEBUG
        # =====================================


        trade_signal = decision.get(

            "signal",

            "HOLD"

        )



        if trade_signal == "HOLD":


            valid = test_df[

                test_df["signal"]

                .isin(

                    [
                        "BUY",
                        "SELL"
                    ]

                )

            ]



            if not valid.empty:


                trade_signal = valid.iloc[-1]["signal"]





        print()


        print(

            "RISK DEBUG SIGNAL:",

            trade_signal

        )



        risk = RiskEngine.calculate(

            test_df,

            trade_signal

        )



        print()


        print(
            "RISK"
        )


        print(

            risk

        )







        # =====================================
        # BACKTEST
        # =====================================


        backtester = Backtester()



        trades = backtester.run(

            test_df

        )



        stats = backtester.statistics()



        print()


        print("=" * 60)

        print(
            "QuantCore Backtest Report"
        )

        print("=" * 60)


        print(

            stats

        )







        # =====================================
        # WALK FORWARD
        # =====================================


        wf = WalkForwardValidator.run(

            df

        )


        print()


        print(
            "Walk Forward"
        )


        print(

            wf

        )





    except Exception as e:


        print()


        print(
            "ERROR:"
        )


        print(

            e

        )



    finally:


        provider.shutdown()





if __name__ == "__main__":


    main()
import pandas as pd

from src.strategy.trend_engine import TrendEngine
from src.strategy.trigger_engine import TriggerEngine


class StrategyEngine:

    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


    @staticmethod
    def generate(df: pd.DataFrame) -> dict:


        if df is None or df.empty:

            return {

                "signal": StrategyEngine.HOLD,
                "trend": TrendEngine.RANGE,
                "trigger": TriggerEngine.HOLD,
                "confidence":0,
                "reason":"No Data"

            }



        last = df.iloc[-1]


        trend = TrendEngine.detect(df)


        trigger = TriggerEngine.detect(df)



        signal = StrategyEngine.HOLD


        confidence = 40


        reasons=[]



        # ==========================
        # RANGE
        # ==========================

        if trend == TrendEngine.RANGE:


            return {

                "signal":"HOLD",

                "trend":trend,

                "trigger":trigger,

                "confidence":30,

                "reason":
                "Range Market"

            }




        # ==========================
        # BULL
        # ==========================


        if trend == TrendEngine.UPTREND:


            reasons.append(
                "Bull Trend"
            )


            if trigger == TriggerEngine.BUY:


                signal="BUY"

                confidence+=30

                reasons.append(
                    "Momentum Confirmed"
                )


            else:


                reasons.append(
                    "Waiting Buy Trigger"
                )





        # ==========================
        # BEAR
        # ==========================


        elif trend == TrendEngine.DOWNTREND:


            reasons.append(
                "Bear Trend"
            )


            if trigger == TriggerEngine.SELL:


                signal="SELL"

                confidence+=30


                reasons.append(
                    "Momentum Confirmed"
                )



            else:


                reasons.append(
                    "Waiting Sell Trigger"
                )





        return {


            "signal":signal,

            "trend":trend,

            "trigger":trigger,

            "confidence":
                min(confidence,100),

            "reason":
                ", ".join(reasons)


        }
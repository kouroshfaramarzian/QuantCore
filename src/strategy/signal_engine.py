from __future__ import annotations

import pandas as pd


class SignalEngine:

    """
    QuantCore Signal Engine V8.1

    Logic:

    BULL:
        Structure BULL
        Fresh BOS <= 3 candles
        MACD > 0
        RSI > 55

        => BUY


    BEAR:
        Structure BEAR
        Fresh BOS <= 3 candles
        MACD < 0
        RSI < 45

        => SELL


    RANGE:
        HOLD
    """


    BASE_CONFIDENCE = 20

    BOS_LOOKBACK = 3


    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"



    @staticmethod
    def has_fresh_bos(
        df: pd.DataFrame,
        structure: str
    ) -> bool:


        if df is None or df.empty:
            return False


        recent = df.tail(
            SignalEngine.BOS_LOOKBACK
        )


        if structure == "BULL":

            if "BULLISH_BOS" not in recent.columns:
                return False


            return bool(
                recent["BULLISH_BOS"].any()
            )



        if structure == "BEAR":

            if "BEARISH_BOS" not in recent.columns:
                return False


            return bool(
                recent["BEARISH_BOS"].any()
            )


        return False




    @staticmethod
    def generate(
        df: pd.DataFrame
    ) -> dict:


        if df is None or df.empty:

            return {

                "signal": SignalEngine.HOLD,
                "trigger": SignalEngine.HOLD,
                "confidence": 0,
                "trend": "RANGE",
                "reason": "No data"

            }



        last = df.iloc[-1]


        structure = str(
            last.get(
                "STRUCTURE",
                "RANGE"
            )
        ).upper()



        confidence = int(
            last.get(
                "STRUCTURE_SCORE",
                SignalEngine.BASE_CONFIDENCE
            )
        )



        macd = float(
            last.get(
                "MACD",
                0
            )
        )


        rsi = float(
            last.get(
                "RSI14",
                50
            )
        )


        choch_bull = bool(
            last.get(
                "CHOCH_BULLISH",
                False
            )
        )


        choch_bear = bool(
            last.get(
                "CHOCH_BEARISH",
                False
            )
        )



        reason = []



        # =========================
        # RANGE
        # =========================

        if structure == "RANGE":

            return {

                "signal": SignalEngine.HOLD,
                "trigger": SignalEngine.HOLD,
                "confidence": confidence,
                "trend": structure,
                "reason": "Range Market"

            }



        # =========================
        # BULL
        # =========================

        if structure == "BULL":


            reason.append(
                "Bull Structure"
            )


            if not SignalEngine.has_fresh_bos(
                df,
                "BULL"
            ):


                reason.append(
                    "Waiting Fresh Bull BOS"
                )


                return {

                    "signal": SignalEngine.HOLD,
                    "trigger": SignalEngine.HOLD,
                    "confidence": confidence,
                    "trend": structure,
                    "reason": ", ".join(reason)

                }



            reason.append(
                "Bull BOS Confirmed"
            )



            if macd > 0 and rsi > 55:


                confidence = min(
                    confidence + 30,
                    100
                )


                reason.append(
                    "MACD Bull"
                )


                reason.append(
                    "RSI Bull"
                )



                if choch_bull:

                    confidence = min(
                        confidence + 10,
                        100
                    )

                    reason.append(
                        "Bull CHOCH"
                    )



                return {

                    "signal": SignalEngine.BUY,
                    "trigger": SignalEngine.BUY,
                    "confidence": confidence,
                    "trend": structure,
                    "reason": ", ".join(reason)

                }



            reason.append(
                "Waiting Momentum"
            )



            return {

                "signal": SignalEngine.HOLD,
                "trigger": SignalEngine.HOLD,
                "confidence": confidence,
                "trend": structure,
                "reason": ", ".join(reason)

            }





        # =========================
        # BEAR
        # =========================

        if structure == "BEAR":


            reason.append(
                "Bear Structure"
            )



            if not SignalEngine.has_fresh_bos(
                df,
                "BEAR"
            ):


                reason.append(
                    "Waiting Fresh Bear BOS"
                )


                return {

                    "signal": SignalEngine.HOLD,
                    "trigger": SignalEngine.HOLD,
                    "confidence": confidence,
                    "trend": structure,
                    "reason": ", ".join(reason)

                }



            reason.append(
                "Bear BOS Confirmed"
            )



            if macd < 0 and rsi < 45:


                confidence = min(
                    confidence + 30,
                    100
                )


                reason.append(
                    "MACD Bear"
                )


                reason.append(
                    "RSI Bear"
                )



                if choch_bear:

                    confidence = min(
                        confidence + 10,
                        100
                    )

                    reason.append(
                        "Bear CHOCH"
                    )



                return {

                    "signal": SignalEngine.SELL,
                    "trigger": SignalEngine.SELL,
                    "confidence": confidence,
                    "trend": structure,
                    "reason": ", ".join(reason)

                }



            reason.append(
                "Waiting Momentum"
            )



            return {

                "signal": SignalEngine.HOLD,
                "trigger": SignalEngine.HOLD,
                "confidence": confidence,
                "trend": structure,
                "reason": ", ".join(reason)

            }



        return {

            "signal": SignalEngine.HOLD,
            "trigger": SignalEngine.HOLD,
            "confidence": confidence,
            "trend": structure,
            "reason": "Unknown Structure"

        }




    @staticmethod
    def generate_series(
        df: pd.DataFrame
    ) -> pd.DataFrame:


        df = df.copy()


        signals = []
        triggers = []
        confidences = []
        trends = []
        reasons = []



        for i in range(len(df)):


            result = SignalEngine.generate(
                df.iloc[:i+1]
            )


            signals.append(
                result["signal"]
            )


            triggers.append(
                result["trigger"]
            )


            confidences.append(
                result["confidence"]
            )


            trends.append(
                result["trend"]
            )


            reasons.append(
                result["reason"]
            )



        df["signal"] = signals
        df["trigger"] = triggers
        df["confidence"] = confidences
        df["trend"] = trends
        df["reason"] = reasons



        return df
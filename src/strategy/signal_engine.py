from __future__ import annotations

import pandas as pd


class SignalEngine:
    """
    QuantCore Signal Engine V4

    تصمیم‌گیری فقط بر اساس:

        StructureEngine
        BOS
        CHOCH
        Momentum

    قوانین:

        RANGE  -> HOLD

        BULL:
            بدون BOS -> HOLD
            BOS + تایید -> BUY

        BEAR:
            بدون BOS -> HOLD
            BOS + تایید -> SELL

    """

    @staticmethod
    def generate(
        df: pd.DataFrame,
    ) -> dict:

        last = df.iloc[-1]


        structure = last.get(
            "STRUCTURE",
            "RANGE"
        )


        bullish_bos = bool(
            last.get(
                "BULLISH_BOS",
                False
            )
        )


        bearish_bos = bool(
            last.get(
                "BEARISH_BOS",
                False
            )
        )


        choch_bullish = bool(
            last.get(
                "CHOCH_BULLISH",
                False
            )
        )


        choch_bearish = bool(
            last.get(
                "CHOCH_BEARISH",
                False
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


        signal = "HOLD"

        trigger = "HOLD"

        confidence = int(
            last.get(
                "STRUCTURE_SCORE",
                0
            )
        )


        reason = []


        # =====================================
        # RANGE
        # =====================================

        if structure == "RANGE":

            reason.append(
                "Range"
            )


        # =====================================
        # BULL
        # =====================================

        elif structure == "BULL":


            reason.append(
                "Bull Structure"
            )


            if not bullish_bos:

                reason.append(
                    "Waiting Bull BOS"
                )


            else:

                reason.append(
                    "Bull BOS"
                )


                confirmation = False


                if choch_bullish:

                    reason.append(
                        "Bull CHOCH"
                    )

                    confirmation = True


                if macd > 0:

                    reason.append(
                        "MACD Bull"
                    )

                    confirmation = True


                if rsi > 55:

                    reason.append(
                        "RSI Bull"
                    )

                    confirmation = True



                if confirmation:

                    signal = "BUY"

                    trigger = "BUY"

                    confidence = min(
                        confidence + 20,
                        100
                    )



        # =====================================
        # BEAR
        # =====================================

        elif structure == "BEAR":


            reason.append(
                "Bear Structure"
            )


            if not bearish_bos:

                reason.append(
                    "Waiting Bear BOS"
                )


            else:

                reason.append(
                    "Bear BOS"
                )


                confirmation = False



                if choch_bearish:

                    reason.append(
                        "Bear CHOCH"
                    )

                    confirmation = True



                if macd < 0:

                    reason.append(
                        "MACD Bear"
                    )

                    confirmation = True



                if rsi < 45:

                    reason.append(
                        "RSI Bear"
                    )

                    confirmation = True



                if confirmation:

                    signal = "SELL"

                    trigger = "SELL"

                    confidence = min(
                        confidence + 20,
                        100
                    )



        return {

            "signal": signal,

            "trigger": trigger,

            "confidence": confidence,

            "trend": structure,

            "reason": ", ".join(reason),

        }



    @staticmethod
    def generate_series(
        df: pd.DataFrame,
    ) -> pd.DataFrame:


        df = df.copy()


        signals = []

        triggers = []

        confidences = []

        trends = []

        reasons = []



        for i in range(
            len(df)
        ):


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
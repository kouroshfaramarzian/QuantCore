from __future__ import annotations


class DecisionEngine:
    """
    QuantCore Decision Engine V5

    Final gate.

    فقط خروجی SignalEngine را بررسی می‌کند.

    جلوگیری از:
        Signal BUY -> Decision HOLD
        Signal SELL -> Decision HOLD
    """


    MIN_CONFIDENCE = 30


    @staticmethod
    def decide(

        signal: str,

        confidence: int,

        trend: str,

        reason: str,

    ) -> dict:


        signal = signal.upper()

        trend = trend.upper()



        # ==========================
        # HOLD
        # ==========================

        if signal == "HOLD":

            return {

                "signal": "HOLD",

                "reason": reason,

                "confidence": confidence,

            }



        # ==========================
        # BUY
        # ==========================

        if signal == "BUY":


            if trend != "BULL":

                return {

                    "signal": "HOLD",

                    "reason": "BUY rejected - trend mismatch",

                    "confidence": confidence,

                }



            if confidence < DecisionEngine.MIN_CONFIDENCE:

                return {

                    "signal": "HOLD",

                    "reason": "BUY low confidence",

                    "confidence": confidence,

                }



            return {

                "signal": "BUY",

                "reason": reason,

                "confidence": confidence,

            }



        # ==========================
        # SELL
        # ==========================

        if signal == "SELL":


            if trend != "BEAR":

                return {

                    "signal": "HOLD",

                    "reason": "SELL rejected - trend mismatch",

                    "confidence": confidence,

                }



            if confidence < DecisionEngine.MIN_CONFIDENCE:

                return {

                    "signal": "HOLD",

                    "reason": "SELL low confidence",

                    "confidence": confidence,

                }



            return {

                "signal": "SELL",

                "reason": reason,

                "confidence": confidence,

            }



        return {

            "signal": "HOLD",

            "reason": "Unknown signal",

            "confidence": 0,

        }
from __future__ import annotations


class DecisionEngine:
    """
    QuantCore Decision Engine V3

    آخرین لایه تصمیم گیری

    فقط خروجی SignalEngine را قبول می‌کند.
    """

    BUY_CONFIDENCE = 70
    SELL_CONFIDENCE = 70

    @staticmethod
    def decide(

        structure: str,

        bullish_bos: bool,

        bearish_bos: bool,

        choch_bullish: bool,

        choch_bearish: bool,

        trigger: str,

        confidence: int,

    ) -> dict:

        # ==========================================
        # RANGE
        # ==========================================

        if structure == "RANGE":

            return {

                "signal": "HOLD",

                "reason": "Range market",

                "confidence": 0,

            }

        # ==========================================
        # BULL
        # ==========================================

        if structure == "BULL":

            if not bullish_bos:

                return {

                    "signal": "HOLD",

                    "reason": "Bull structure waiting confirmation",

                    "confidence": confidence,

                }

            if trigger != "BUY":

                return {

                    "signal": "HOLD",

                    "reason": "Bull structure but no BUY trigger",

                    "confidence": confidence,

                }

            if confidence < DecisionEngine.BUY_CONFIDENCE:

                return {

                    "signal": "HOLD",

                    "reason": "Low confidence",

                    "confidence": confidence,

                }

            return {

                "signal": "BUY",

                "reason": "Bull BOS confirmed",

                "confidence": confidence,

            }

        # ==========================================
        # BEAR
        # ==========================================

        if structure == "BEAR":

            if not bearish_bos:

                return {

                    "signal": "HOLD",

                    "reason": "Bear structure waiting confirmation",

                    "confidence": confidence,

                }

            if trigger != "SELL":

                return {

                    "signal": "HOLD",

                    "reason": "Bear structure but no SELL trigger",

                    "confidence": confidence,

                }

            if confidence < DecisionEngine.SELL_CONFIDENCE:

                return {

                    "signal": "HOLD",

                    "reason": "Low confidence",

                    "confidence": confidence,

                }

            return {

                "signal": "SELL",

                "reason": "Bear BOS confirmed",

                "confidence": confidence,

            }

        # ==========================================

        return {

            "signal": "HOLD",

            "reason": "Unknown",

            "confidence": 0,

        }
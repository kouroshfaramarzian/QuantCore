from __future__ import annotations

import pandas as pd


class SignalEngine:
    """
    QuantCore Signal Engine V2.1

    Decision priority:

    1. Market Structure
    2. BOS / CHOCH
    3. Momentum
    4. EMA confirmation

    Never trade against structure.
    """

    @staticmethod
    def generate_series(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df = df.copy()

        results = []

        for _, row in df.iterrows():

            results.append(
                SignalEngine._evaluate(row)
            )


        df["signal"] = [
            x["signal"]
            for x in results
        ]

        df["confidence"] = [
            x["confidence"]
            for x in results
        ]

        df["reason"] = [
            x["reason"]
            for x in results
        ]

        return df



    @staticmethod
    def generate(
        df: pd.DataFrame,
    ) -> dict:

        last = df.iloc[-1]

        return SignalEngine._evaluate(
            last
        )



    @staticmethod
    def _evaluate(
        row,
    ) -> dict:


        structure = row.get(
            "STRUCTURE",
            "RANGE"
        )


        bullish_bos = bool(
            row.get(
                "BULLISH_BOS",
                False
            )
        )

        bearish_bos = bool(
            row.get(
                "BEARISH_BOS",
                False
            )
        )


        bullish_choch = bool(
            row.get(
                "CHOCH_BULLISH",
                False
            )
        )

        bearish_choch = bool(
            row.get(
                "CHOCH_BEARISH",
                False
            )
        )


        macd = row.get(
            "MACD",
            0
        )

        macd_signal = row.get(
            "MACD_SIGNAL",
            0
        )


        rsi = row.get(
            "RSI14",
            50
        )


        ema20 = row.get(
            "EMA20",
            0
        )

        ema50 = row.get(
            "EMA50",
            0
        )

        ema200 = row.get(
            "EMA200",
            0
        )


        buy_score = 0

        sell_score = 0

        reasons = []



        # =========================
        # STRUCTURE
        # =========================

        if structure == "BULL":

            buy_score += 40

            reasons.append(
                "Bull Structure"
            )


        elif structure == "BEAR":

            sell_score += 40

            reasons.append(
                "Bear Structure"
            )



        # =========================
        # BOS
        # =========================

        if bullish_bos:

            buy_score += 25

            reasons.append(
                "Bullish BOS"
            )


        if bearish_bos:

            sell_score += 25

            reasons.append(
                "Bearish BOS"
            )



        # =========================
        # CHOCH
        # =========================

        if bullish_choch:

            buy_score += 15

            reasons.append(
                "Bullish CHOCH"
            )


        if bearish_choch:

            sell_score += 15

            reasons.append(
                "Bearish CHOCH"
            )



        # =========================
        # MACD
        # =========================

        if macd > macd_signal:

            buy_score += 10

            reasons.append(
                "MACD Bull"
            )

        else:

            sell_score += 10

            reasons.append(
                "MACD Bear"
            )



        # =========================
        # RSI
        # =========================

        if rsi < 45:

            sell_score += 5

            reasons.append(
                "RSI Weak"
            )


        elif rsi > 55:

            buy_score += 5

            reasons.append(
                "RSI Strong"
            )



        # =========================
        # EMA
        # =========================

        if (
            ema20 >
            ema50 >
            ema200
        ):

            buy_score += 10

            reasons.append(
                "EMA Bull"
            )


        elif (
            ema20 <
            ema50 <
            ema200
        ):

            sell_score += 10

            reasons.append(
                "EMA Bear"
            )



        # =========================
        # FINAL DECISION
        # =========================


        if buy_score >= 65:

            return {

                "signal": "BUY",

                "trend": structure,

                "trigger": "BUY",

                "confidence": buy_score,

                "buy_score": buy_score,

                "sell_score": sell_score,

                "reason": ", ".join(reasons),

            }



        if sell_score >= 65:

            return {

                "signal": "SELL",

                "trend": structure,

                "trigger": "SELL",

                "confidence": sell_score,

                "buy_score": buy_score,

                "sell_score": sell_score,

                "reason": ", ".join(reasons),

            }



        return {

            "signal": "HOLD",

            "trend": structure,

            "trigger": "NONE",

            "confidence": max(
                buy_score,
                sell_score
            ),

            "buy_score": buy_score,

            "sell_score": sell_score,

            "reason": ", ".join(reasons),

        }
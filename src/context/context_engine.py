import pandas as pd

from src.context.market_context import MarketContext


class ContextEngine:
    """
    Builds a high-level market context from features.
    """

    @staticmethod
    def build(
        df: pd.DataFrame,
    ) -> MarketContext:

        last = df.iloc[-1]

        # -----------------------------
        # Trend
        # -----------------------------

        if (
            last["EMA20"]
            > last["EMA50"]
            > last["EMA200"]
        ):

            trend = "BULL"

        elif (
            last["EMA20"]
            < last["EMA50"]
            < last["EMA200"]
        ):

            trend = "BEAR"

        else:

            trend = "RANGE"

        # -----------------------------
        # Momentum
        # -----------------------------

        if last["RSI14"] >= 60:

            momentum = "STRONG_BULL"

        elif last["RSI14"] <= 40:

            momentum = "STRONG_BEAR"

        else:

            momentum = "NEUTRAL"

        # -----------------------------
        # Volatility
        # -----------------------------

        atr_mean = df["ATR14"].tail(50).mean()

        if last["ATR14"] > atr_mean:

            volatility = "HIGH"

        else:

            volatility = "LOW"

        # -----------------------------
        # Session
        # -----------------------------

        hour = last["time"].hour

        if 7 <= hour < 15:

            session = "LONDON"

        elif 13 <= hour < 22:

            session = "NEWYORK"

        else:

            session = "ASIA"

        return MarketContext(

            trend=trend,

            momentum=momentum,

            volatility=volatility,

            session=session,

        )
from __future__ import annotations

from datetime import datetime

import pandas as pd

from src.context.market_context import MarketContext


class ContextEngine:
    """
    QuantCore Context Engine V2

    این کلاس دیگر روند را محاسبه نمی‌کند.

    فقط خروجی StructureEngine را می‌خواند.
    """

    @staticmethod
    def build(df: pd.DataFrame) -> MarketContext:

        last = df.iloc[-1]

        # =====================================
        # Trend
        # =====================================

        trend = last.get("STRUCTURE", "RANGE")

        # =====================================
        # Momentum
        # =====================================

        rsi = float(last.get("RSI14", 50))

        if rsi >= 60:

            momentum = "BULLISH"

        elif rsi <= 40:

            momentum = "BEARISH"

        else:

            momentum = "NEUTRAL"

        # =====================================
        # Volatility
        # =====================================

        atr = float(last.get("ATR14", 0))

        atr_mean = df["ATR14"].tail(50).mean()

        if atr > atr_mean:

            volatility = "HIGH"

        else:

            volatility = "LOW"

        # =====================================
        # Session
        # =====================================

        t = last["time"]

        if isinstance(t, pd.Timestamp):

            hour = t.hour

        elif isinstance(t, datetime):

            hour = t.hour

        else:

            hour = datetime.now().hour

        if 7 <= hour < 15:

            session = "LONDON"

        elif 13 <= hour < 22:

            session = "NEWYORK"

        else:

            session = "ASIA"

        # =====================================
        # Confidence
        # =====================================

        confidence = int(last.get("STRUCTURE_SCORE", 0))

        # =====================================

        return MarketContext(

            trend=trend,

            momentum=momentum,

            volatility=volatility,

            session=session,

            confidence=confidence,

            source="StructureEngine",

        )
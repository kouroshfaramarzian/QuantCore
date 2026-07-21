import pandas as pd

from src.strategy.conditions import Conditions


class SignalEngine:
    """
    Generates BUY / SELL / HOLD signals.
    """

    @staticmethod
    def generate(
        df: pd.DataFrame,
    ) -> str:

        if (
            Conditions.ema_bullish(df)
            and Conditions.macd_bullish(df)
            and Conditions.rsi_bullish(df)
            and Conditions.bullish_candle(df)
        ):
            return "BUY"

        if (
            Conditions.ema_bearish(df)
            and Conditions.macd_bearish(df)
            and Conditions.rsi_bearish(df)
            and Conditions.bearish_candle(df)
        ):
            return "SELL"

        return "HOLD"
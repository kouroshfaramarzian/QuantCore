import pandas as pd

from src.strategy.conditions import Conditions


class TriggerEngine:

    BUY = "BUY"

    SELL = "SELL"

    HOLD = "HOLD"

    @staticmethod
    def detect(df: pd.DataFrame):

        buy = 0
        sell = 0

        if Conditions.macd_bullish(df):
            buy += 1

        if Conditions.rsi_bullish(df):
            buy += 1

        if Conditions.bullish_candle(df):
            buy += 1

        if Conditions.macd_bearish(df):
            sell += 1

        if Conditions.rsi_bearish(df):
            sell += 1

        if Conditions.bearish_candle(df):
            sell += 1

        if buy >= 2 and buy > sell:
            return TriggerEngine.BUY

        if sell >= 2 and sell > buy:
            return TriggerEngine.SELL

        return TriggerEngine.HOLD
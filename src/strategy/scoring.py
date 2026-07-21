from src.strategy.conditions import Conditions


class Scoring:

    """
    Signal scoring system.
    """

    @staticmethod
    def buy_score(df):

        score = 0

        if Conditions.ema_bullish(df):
            score += 30

        if Conditions.macd_bullish(df):
            score += 25

        if Conditions.rsi_bullish(df):
            score += 20

        if Conditions.bullish_candle(df):
            score += 25

        return score

    @staticmethod
    def sell_score(df):

        score = 0

        if Conditions.ema_bearish(df):
            score += 30

        if Conditions.macd_bearish(df):
            score += 25

        if Conditions.rsi_bearish(df):
            score += 20

        if Conditions.bearish_candle(df):
            score += 25

        return score
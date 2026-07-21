import pandas as pd


class Conditions:
    """
    Entry conditions used by Signal Engine.
    """

    @staticmethod
    def ema_bullish(df: pd.DataFrame) -> bool:
        last = df.iloc[-1]
        return (
            last["EMA20"] > last["EMA50"]
            and last["EMA50"] > last["EMA200"]
        )

    @staticmethod
    def ema_bearish(df: pd.DataFrame) -> bool:
        last = df.iloc[-1]
        return (
            last["EMA20"] < last["EMA50"]
            and last["EMA50"] < last["EMA200"]
        )

    @staticmethod
    def rsi_bullish(df: pd.DataFrame) -> bool:
        return df.iloc[-1]["RSI14"] > 55

    @staticmethod
    def rsi_bearish(df: pd.DataFrame) -> bool:
        return df.iloc[-1]["RSI14"] < 45

    @staticmethod
    def macd_bullish(df: pd.DataFrame) -> bool:
        last = df.iloc[-1]
        return last["MACD"] > last["MACD_SIGNAL"]

    @staticmethod
    def macd_bearish(df: pd.DataFrame) -> bool:
        last = df.iloc[-1]
        return last["MACD"] < last["MACD_SIGNAL"]

    @staticmethod
    def bullish_candle(df: pd.DataFrame) -> bool:
        return bool(df.iloc[-1]["IS_BULLISH"])

    @staticmethod
    def bearish_candle(df: pd.DataFrame) -> bool:
        return bool(df.iloc[-1]["IS_BEARISH"])
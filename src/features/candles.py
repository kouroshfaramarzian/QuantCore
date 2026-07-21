import pandas as pd


class CandleFeatures:

    @staticmethod
    def body(df: pd.DataFrame) -> pd.Series:
        return (df["close"] - df["open"]).abs()

    @staticmethod
    def upper_wick(df: pd.DataFrame) -> pd.Series:
        return df["high"] - df[["open", "close"]].max(axis=1)

    @staticmethod
    def lower_wick(df: pd.DataFrame) -> pd.Series:
        return df[["open", "close"]].min(axis=1) - df["low"]

    @staticmethod
    def candle_range(df: pd.DataFrame) -> pd.Series:
        return df["high"] - df["low"]

    @staticmethod
    def bullish(df: pd.DataFrame) -> pd.Series:
        return df["close"] > df["open"]

    @staticmethod
    def bearish(df: pd.DataFrame) -> pd.Series:
        return df["close"] < df["open"]

    @staticmethod
    def body_percent(df: pd.DataFrame) -> pd.Series:
        body = (df["close"] - df["open"]).abs()
        rng = df["high"] - df["low"]

        return body / rng.replace(0, 1)
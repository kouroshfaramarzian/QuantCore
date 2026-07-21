import pandas as pd


class VolatilityIndicators:

    @staticmethod
    def atr(
        df: pd.DataFrame,
        period: int = 14,
    ) -> pd.Series:

        high_low = df["high"] - df["low"]

        high_close = (
            df["high"] - df["close"].shift()
        ).abs()

        low_close = (
            df["low"] - df["close"].shift()
        ).abs()

        tr = pd.concat(
            [
                high_low,
                high_close,
                low_close,
            ],
            axis=1,
        ).max(axis=1)

        return tr.rolling(period).mean()

    @staticmethod
    def bollinger(
        df: pd.DataFrame,
        period: int = 20,
        std: float = 2,
        column: str = "close",
    ):

        middle = (
            df[column]
            .rolling(period)
            .mean()
        )

        deviation = (
            df[column]
            .rolling(period)
            .std()
        )

        upper = middle + std * deviation

        lower = middle - std * deviation

        return upper, middle, lower
import pandas as pd


class TrendIndicators:

    @staticmethod
    def ema(
        df: pd.DataFrame,
        period: int,
        column: str = "close",
    ) -> pd.Series:

        return (
            df[column]
            .ewm(
                span=period,
                adjust=False,
            )
            .mean()
        )

    @staticmethod
    def macd(
        df: pd.DataFrame,
        column: str = "close",
        fast: int = 12,
        slow: int = 26,
        signal: int = 9,
    ):

        ema_fast = (
            df[column]
            .ewm(span=fast, adjust=False)
            .mean()
        )

        ema_slow = (
            df[column]
            .ewm(span=slow, adjust=False)
            .mean()
        )

        macd = ema_fast - ema_slow

        signal_line = (
            macd
            .ewm(span=signal, adjust=False)
            .mean()
        )

        histogram = macd - signal_line

        return macd, signal_line, histogram
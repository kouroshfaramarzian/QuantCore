import pandas as pd


class Indicators:
    """
    Technical indicators for QuantCore.
    """

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
    def rsi(
        df: pd.DataFrame,
        period: int = 14,
        column: str = "close",
    ) -> pd.Series:

        delta = df[column].diff()

        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.ewm(
            alpha=1 / period,
            adjust=False,
        ).mean()

        avg_loss = loss.ewm(
            alpha=1 / period,
            adjust=False,
        ).mean()

        rs = avg_gain / avg_loss

        return 100 - (100 / (1 + rs))

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
    def macd(
        df: pd.DataFrame,
        column: str = "close",
        fast: int = 12,
        slow: int = 26,
        signal: int = 9,
    ) -> tuple:

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

    @staticmethod
    def bollinger(
        df: pd.DataFrame,
        period: int = 20,
        std: float = 2,
        column: str = "close",
    ) -> tuple:

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
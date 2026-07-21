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
        """
        Relative Strength Index (RSI)
        """

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

        rsi = 100 - (100 / (1 + rs))

        return rsi
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
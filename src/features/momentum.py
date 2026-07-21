import pandas as pd


class MomentumIndicators:

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
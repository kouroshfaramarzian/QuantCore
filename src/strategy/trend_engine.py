import pandas as pd


class TrendEngine:

    UPTREND = "UP"

    DOWNTREND = "DOWN"

    RANGE = "RANGE"

    @staticmethod
    def detect(df: pd.DataFrame):

        last = df.iloc[-1]

        if (
            last["EMA20"]
            > last["EMA50"]
            > last["EMA200"]
        ):

            return TrendEngine.UPTREND

        if (
            last["EMA20"]
            < last["EMA50"]
            < last["EMA200"]
        ):

            return TrendEngine.DOWNTREND

        return TrendEngine.RANGE
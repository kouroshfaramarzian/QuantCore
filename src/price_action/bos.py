from __future__ import annotations

import pandas as pd


class BOSDetector:

    """
    Break Of Structure
    """

    @staticmethod
    def detect(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df = df.copy()

        df["BOS_UP"] = False
        df["BOS_DOWN"] = False

        last_high = None
        last_low = None

        for i in range(len(df)):

            if df.iloc[i]["SWING_HIGH"]:
                last_high = df.iloc[i]["high"]

            if df.iloc[i]["SWING_LOW"]:
                last_low = df.iloc[i]["low"]

            if last_high is not None:

                if df.iloc[i]["close"] > last_high:

                    df.iat[
                        i,
                        df.columns.get_loc("BOS_UP")
                    ] = True

            if last_low is not None:

                if df.iloc[i]["close"] < last_low:

                    df.iat[
                        i,
                        df.columns.get_loc("BOS_DOWN")
                    ] = True

        return df
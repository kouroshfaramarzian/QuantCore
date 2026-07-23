from __future__ import annotations

import pandas as pd


class CHOCHDetector:

    """
    Change Of Character
    """

    @staticmethod
    def detect(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df = df.copy()

        df["CHOCH_UP"] = False
        df["CHOCH_DOWN"] = False

        trend = None

        for i in range(len(df)):

            if df.iloc[i]["BOS_UP"]:

                if trend == "DOWN":

                    df.iat[
                        i,
                        df.columns.get_loc("CHOCH_UP")
                    ] = True

                trend = "UP"

            elif df.iloc[i]["BOS_DOWN"]:

                if trend == "UP":

                    df.iat[
                        i,
                        df.columns.get_loc("CHOCH_DOWN")
                    ] = True

                trend = "DOWN"

        return df
from __future__ import annotations

import pandas as pd


class BOSDetector:
    """
    Break Of Structure Detector

    Requires:

        SWING_HIGH
        SWING_LOW
    """

    @staticmethod
    def detect(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df = df.copy()

        df["BULLISH_BOS"] = False
        df["BEARISH_BOS"] = False

        last_swing_high = None
        last_swing_low = None

        for i in range(len(df)):

            row = df.iloc[i]

            if row["SWING_HIGH"]:
                last_swing_high = row["high"]

            if row["SWING_LOW"]:
                last_swing_low = row["low"]

            if last_swing_high is not None:

                if row["close"] > last_swing_high:

                    df.at[df.index[i], "BULLISH_BOS"] = True

                    last_swing_high = row["close"]

            if last_swing_low is not None:

                if row["close"] < last_swing_low:

                    df.at[df.index[i], "BEARISH_BOS"] = True

                    last_swing_low = row["close"]

        return df
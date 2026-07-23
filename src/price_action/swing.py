from __future__ import annotations

import pandas as pd


class SwingDetector:
    """
    Detect Swing High / Swing Low
    """

    @staticmethod
    def detect(
        df: pd.DataFrame,
        left: int = 3,
        right: int = 3,
    ) -> pd.DataFrame:

        df = df.copy()

        df["SWING_HIGH"] = False
        df["SWING_LOW"] = False

        highs = df["high"].values
        lows = df["low"].values

        for i in range(left, len(df) - right):

            current_high = highs[i]
            current_low = lows[i]

            left_high = highs[i-left:i]
            right_high = highs[i+1:i+right+1]

            left_low = lows[i-left:i]
            right_low = lows[i+1:i+right+1]

            if (
                current_high > left_high.max()
                and current_high > right_high.max()
            ):
                df.at[df.index[i], "SWING_HIGH"] = True

            if (
                current_low < left_low.min()
                and current_low < right_low.min()
            ):
                df.at[df.index[i], "SWING_LOW"] = True

        return df
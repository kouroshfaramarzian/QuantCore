from __future__ import annotations

import pandas as pd
import numpy as np


class SwingDetector:
    """
    QuantCore Swing Detector V2

    Smart Money Concept Swing Detection

    خروجی:

        SWING_HIGH
        SWING_LOW

        LAST_SWING_HIGH
        LAST_SWING_LOW

        SWING_TYPE
    """

    @staticmethod
    def detect(

        df: pd.DataFrame,

        left: int = 3,

        right: int = 3,

    ) -> pd.DataFrame:


        df = df.copy()

        size = len(df)

        swing_high = np.zeros(size, dtype=bool)

        swing_low = np.zeros(size, dtype=bool)

        swing_type = np.full(size, "", dtype=object)

        highs = df["high"].values
        lows = df["low"].values


        # ---------------------------------------
        # Pivot Detection
        # ---------------------------------------

        for i in range(left, size - right):

            current_high = highs[i]

            current_low = lows[i]

            left_high = highs[i-left:i]

            right_high = highs[i+1:i+right+1]

            left_low = lows[i-left:i]

            right_low = lows[i+1:i+right+1]


            if (

                current_high > left_high.max()

                and

                current_high >= right_high.max()

            ):

                swing_high[i] = True

                swing_type[i] = "HH"


            if (

                current_low < left_low.min()

                and

                current_low <= right_low.min()

            ):

                swing_low[i] = True

                swing_type[i] = "LL"


        df["SWING_HIGH"] = swing_high

        df["SWING_LOW"] = swing_low

        df["SWING_TYPE"] = swing_type


        # ---------------------------------------
        # Last Swing Levels
        # ---------------------------------------

        last_high = np.nan

        last_low = np.nan

        last_high_series = []

        last_low_series = []


        for i in range(size):

            if swing_high[i]:

                last_high = highs[i]

            if swing_low[i]:

                last_low = lows[i]

            last_high_series.append(last_high)

            last_low_series.append(last_low)


        df["LAST_SWING_HIGH"] = last_high_series

        df["LAST_SWING_LOW"] = last_low_series


        return df
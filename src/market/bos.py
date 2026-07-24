from __future__ import annotations

import pandas as pd


class BOSDetector:
    """
    QuantCore BOS Detector V4

    Uses SwingDetector output.

    Required Columns
    ----------------
    SWING_HIGH
    SWING_LOW
    SWING_HIGH_PRICE
    SWING_LOW_PRICE

    Output
    ------
    BULLISH_BOS
    BEARISH_BOS

    BOS_LEVEL
    BOS_DIRECTION

    LAST_STRUCTURE_HIGH
    LAST_STRUCTURE_LOW
    """

    @staticmethod
    def detect(df: pd.DataFrame) -> pd.DataFrame:

        df = df.copy()

        df["BULLISH_BOS"] = False
        df["BEARISH_BOS"] = False

        df["BOS_LEVEL"] = None
        df["BOS_DIRECTION"] = None

        df["LAST_STRUCTURE_HIGH"] = None
        df["LAST_STRUCTURE_LOW"] = None

        structure_high = None
        structure_low = None

        last_break = None

        for i in range(len(df)):

            row = df.iloc[i]

            # ---------------------------------
            # Update latest confirmed swings
            # ---------------------------------

            if row["SWING_HIGH"]:

                structure_high = row["SWING_HIGH_PRICE"]

            if row["SWING_LOW"]:

                structure_low = row["SWING_LOW_PRICE"]

            df.at[df.index[i], "LAST_STRUCTURE_HIGH"] = structure_high
            df.at[df.index[i], "LAST_STRUCTURE_LOW"] = structure_low

            close = row["close"]

            # ---------------------------------
            # Bull BOS
            # ---------------------------------

            if structure_high is not None:

                if close > structure_high:

                    if last_break != "BULL":

                        df.at[df.index[i], "BULLISH_BOS"] = True

                        df.at[df.index[i], "BOS_LEVEL"] = structure_high

                        df.at[df.index[i], "BOS_DIRECTION"] = "BULL"

                        last_break = "BULL"

            # ---------------------------------
            # Bear BOS
            # ---------------------------------

            if structure_low is not None:

                if close < structure_low:

                    if last_break != "BEAR":

                        df.at[df.index[i], "BEARISH_BOS"] = True

                        df.at[df.index[i], "BOS_LEVEL"] = structure_low

                        df.at[df.index[i], "BOS_DIRECTION"] = "BEAR"

                        last_break = "BEAR"

            # ---------------------------------
            # Reset when opposite structure breaks
            # ---------------------------------

            if (
                last_break == "BULL"
                and structure_low is not None
                and close < structure_low
            ):
                last_break = None

            elif (
                last_break == "BEAR"
                and structure_high is not None
                and close > structure_high
            ):
                last_break = None

        return df
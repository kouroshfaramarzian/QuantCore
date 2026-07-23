from __future__ import annotations

import pandas as pd


class CHOCHDetector:
    """
    Change Of Character Detector

    Detects market structure change.

    Bear structure:
        bearish BOS -> trend down

    Bullish CHOCH:
        price breaks previous swing high
        while structure was bearish

    Bearish CHOCH:
        price breaks previous swing low
        while structure was bullish
    """

    @staticmethod
    def detect(
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        df = df.copy()

        df["CHOCH_BULLISH"] = False
        df["CHOCH_BEARISH"] = False
        df["STRUCTURE"] = "RANGE"

        structure = "RANGE"

        last_swing_high = None
        last_swing_low = None


        for i in range(len(df)):

            row = df.iloc[i]


            if row["SWING_HIGH"]:

                last_swing_high = row["high"]


            if row["SWING_LOW"]:

                last_swing_low = row["low"]



            # =========================
            # Bearish structure
            # =========================

            if structure == "BEAR":

                if (
                    last_swing_high is not None
                    and row["close"] > last_swing_high
                ):

                    df.at[
                        df.index[i],
                        "CHOCH_BULLISH"
                    ] = True


                    structure = "BULL"



            # =========================
            # Bullish structure
            # =========================

            elif structure == "BULL":

                if (
                    last_swing_low is not None
                    and row["close"] < last_swing_low
                ):

                    df.at[
                        df.index[i],
                        "CHOCH_BEARISH"
                    ] = True


                    structure = "BEAR"



            # =========================
            # Initial detection
            # =========================

            else:

                if (
                    last_swing_high is not None
                    and row["close"] > last_swing_high
                ):

                    structure = "BULL"


                elif (
                    last_swing_low is not None
                    and row["close"] < last_swing_low
                ):

                    structure = "BEAR"



            df.at[
                df.index[i],
                "STRUCTURE"
            ] = structure


        return df
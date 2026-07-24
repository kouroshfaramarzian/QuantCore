from __future__ import annotations

import pandas as pd


class CHOCHDetector:
    """
    QuantCore CHOCH Detector V2

    Change Of Character

    نیازمند:

        BULLISH_BOS
        BEARISH_BOS
        STRUCTURE

    خروجی:

        CHOCH_BULLISH
        CHOCH_BEARISH

        CHOCH_LEVEL
        CHOCH_DIRECTION
    """

    @staticmethod
    def detect(df: pd.DataFrame) -> pd.DataFrame:

        df = df.copy()

        df["CHOCH_BULLISH"] = False
        df["CHOCH_BEARISH"] = False

        df["CHOCH_LEVEL"] = None
        df["CHOCH_DIRECTION"] = None

        previous_structure = None

        for i in range(len(df)):

            row = df.iloc[i]

            structure = row.get("STRUCTURE", "RANGE")

            bull_bos = bool(row.get("BULLISH_BOS", False))
            bear_bos = bool(row.get("BEARISH_BOS", False))

            # اولین مقدار
            if previous_structure is None:
                previous_structure = structure
                continue

            # -----------------------------------
            # BEAR -> BULL
            # -----------------------------------

            if (
                previous_structure == "BEAR"
                and structure == "BULL"
                and bull_bos
            ):

                df.at[df.index[i], "CHOCH_BULLISH"] = True

                df.at[df.index[i], "CHOCH_DIRECTION"] = "BULL"

                df.at[df.index[i], "CHOCH_LEVEL"] = row.get(
                    "LAST_STRUCTURE_HIGH"
                )

            # -----------------------------------
            # BULL -> BEAR
            # -----------------------------------

            elif (
                previous_structure == "BULL"
                and structure == "BEAR"
                and bear_bos
            ):

                df.at[df.index[i], "CHOCH_BEARISH"] = True

                df.at[df.index[i], "CHOCH_DIRECTION"] = "BEAR"

                df.at[df.index[i], "CHOCH_LEVEL"] = row.get(
                    "LAST_STRUCTURE_LOW"
                )

            previous_structure = structure

        return df
from __future__ import annotations

import pandas as pd


class BOSDetector:
    """
    QuantCore BOS Detector V2

    Break Of Structure

    Rules:

    Bullish BOS:
        close breaks previous swing high

    Bearish BOS:
        close breaks previous swing low

    Requires:

        LAST_SWING_HIGH
        LAST_SWING_LOW
    """

    @staticmethod
    def detect(

        df: pd.DataFrame,

    ) -> pd.DataFrame:


        df = df.copy()


        df["BULLISH_BOS"] = False

        df["BEARISH_BOS"] = False


        structure = []


        current_structure = "RANGE"


        last_broken_high = None

        last_broken_low = None



        for i in range(len(df)):


            row = df.iloc[i]


            close = row["close"]


            swing_high = row.get(
                "LAST_SWING_HIGH",
                None
            )


            swing_low = row.get(
                "LAST_SWING_LOW",
                None
            )



            # =============================
            # BULLISH BOS
            # =============================

            if swing_high is not None:


                if (

                    close > swing_high

                    and

                    swing_high != last_broken_high

                ):


                    df.at[
                        df.index[i],
                        "BULLISH_BOS"
                    ] = True


                    current_structure = "BULL"

                    last_broken_high = swing_high



            # =============================
            # BEARISH BOS
            # =============================

            if swing_low is not None:


                if (

                    close < swing_low

                    and

                    swing_low != last_broken_low

                ):


                    df.at[
                        df.index[i],
                        "BEARISH_BOS"
                    ] = True


                    current_structure = "BEAR"

                    last_broken_low = swing_low



            structure.append(
                current_structure
            )



        df["STRUCTURE"] = structure


        return df
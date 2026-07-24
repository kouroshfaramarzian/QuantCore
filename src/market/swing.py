from __future__ import annotations

import pandas as pd


class SwingDetector:
    """
    QuantCore Swing Detector V2

    خروجی:

    SWING_HIGH
    SWING_LOW

    SWING_HIGH_PRICE
    SWING_LOW_PRICE

    LAST_SWING_HIGH
    LAST_SWING_LOW

    SWING_STRENGTH
    """

    @staticmethod
    def detect(
        df: pd.DataFrame,
        left: int = 3,
        right: int = 3,
        min_distance: float = 0.3,
    ) -> pd.DataFrame:

        df = df.copy()

        df["SWING_HIGH"] = False
        df["SWING_LOW"] = False

        df["SWING_HIGH_PRICE"] = None
        df["SWING_LOW_PRICE"] = None

        df["LAST_SWING_HIGH"] = None
        df["LAST_SWING_LOW"] = None

        df["SWING_STRENGTH"] = 0.0

        highs = df["high"].values
        lows = df["low"].values

        last_high = None
        last_low = None

        for i in range(left, len(df) - right):

            current_high = highs[i]
            current_low = lows[i]

            left_high = highs[i-left:i]
            right_high = highs[i+1:i+right+1]

            left_low = lows[i-left:i]
            right_low = lows[i+1:i+right+1]

            # -------------------------
            # Swing High
            # -------------------------

            if (
                current_high > left_high.max()
                and current_high > right_high.max()
            ):

                if (
                    last_high is None
                    or abs(current_high - last_high) >= min_distance
                ):

                    df.at[df.index[i], "SWING_HIGH"] = True
                    df.at[df.index[i], "SWING_HIGH_PRICE"] = current_high

                    strength = (
                        current_high
                        - max(left_high.max(), right_high.max())
                    )

                    df.at[df.index[i], "SWING_STRENGTH"] = round(strength, 3)

                    last_high = current_high

            # -------------------------
            # Swing Low
            # -------------------------

            if (
                current_low < left_low.min()
                and current_low < right_low.min()
            ):

                if (
                    last_low is None
                    or abs(current_low - last_low) >= min_distance
                ):

                    df.at[df.index[i], "SWING_LOW"] = True
                    df.at[df.index[i], "SWING_LOW_PRICE"] = current_low

                    strength = (
                        min(left_low.min(), right_low.min())
                        - current_low
                    )

                    df.at[df.index[i], "SWING_STRENGTH"] = round(strength, 3)

                    last_low = current_low

            # -------------------------
            # Save Last Swings
            # -------------------------

            df.at[df.index[i], "LAST_SWING_HIGH"] = last_high
            df.at[df.index[i], "LAST_SWING_LOW"] = last_low

        return df
from __future__ import annotations

import pandas as pd


class PullbackEngine:
    """
    QuantCore Pullback Engine V1

    Logic:

    BOS
        |
        ↓
    Wait for retest
        |
        ↓
    Confirmation candle
        |
        ↓
    Trigger BUY / SELL
    """


    @staticmethod
    def generate(
        df: pd.DataFrame,
        tolerance: float = 0.001
    ) -> pd.DataFrame:


        df = df.copy()


        df["trigger"] = "HOLD"


        waiting_bull_pullback = False
        waiting_bear_pullback = False


        bos_level = None



        for i in range(len(df)):


            row = df.iloc[i]



            # =====================================
            # Detect Bull BOS
            # =====================================

            if row.get(
                "BULLISH_BOS",
                False
            ):


                waiting_bull_pullback = True

                waiting_bear_pullback = False

                bos_level = row.get(
                    "BOS_LEVEL"
                )



            # =====================================
            # Detect Bear BOS
            # =====================================

            if row.get(
                "BEARISH_BOS",
                False
            ):


                waiting_bear_pullback = True

                waiting_bull_pullback = False

                bos_level = row.get(
                    "BOS_LEVEL"
                )



            if bos_level is None:

                continue



            close = row["close"]

            high = row["high"]

            low = row["low"]



            # =====================================
            # Bull Pullback
            # =====================================

            if waiting_bull_pullback:


                distance = abs(
                    close - bos_level
                ) / bos_level



                if distance <= tolerance:


                    # bullish candle confirmation

                    if close > row["open"]:


                        df.at[
                            df.index[i],
                            "trigger"
                        ] = "BUY"


                        waiting_bull_pullback = False



            # =====================================
            # Bear Pullback
            # =====================================

            if waiting_bear_pullback:


                distance = abs(
                    close - bos_level
                ) / bos_level



                if distance <= tolerance:


                    if close < row["open"]:


                        df.at[
                            df.index[i],
                            "trigger"
                        ] = "SELL"


                        waiting_bear_pullback = False



        return df
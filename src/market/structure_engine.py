from __future__ import annotations

import pandas as pd


class StructureEngine:
    """
    QuantCore Structure Engine V5

    Stateful Structure Memory

    حفظ:
        BOS
        CHOCH
        Structure

    """

    BULL_THRESHOLD = 40
    BEAR_THRESHOLD = 40


    @staticmethod
    def build(
        df: pd.DataFrame
    ) -> pd.DataFrame:


        df = df.copy()


        df["STRUCTURE"] = "RANGE"

        df["STRUCTURE_SCORE"] = 0

        df["STRUCTURE_REASON"] = ""


        # حفظ رویداد ساختاری

        df["STRUCTURE_BULL_BOS"] = False

        df["STRUCTURE_BEAR_BOS"] = False

        df["STRUCTURE_BULL_CHOCH"] = False

        df["STRUCTURE_BEAR_CHOCH"] = False



        current_structure = "RANGE"

        current_score = 0

        current_reason = ""



        last_bull_bos = False

        last_bear_bos = False

        last_bull_choch = False

        last_bear_choch = False



        for i in range(len(df)):


            row = df.iloc[i]


            bull_score = 0

            bear_score = 0


            bull_reason = []

            bear_reason = []



            bull_bos = bool(
                row.get(
                    "BULLISH_BOS",
                    False
                )
            )


            bear_bos = bool(
                row.get(
                    "BEARISH_BOS",
                    False
                )
            )



            bull_choch = bool(
                row.get(
                    "CHOCH_BULLISH",
                    False
                )
            )


            bear_choch = bool(
                row.get(
                    "CHOCH_BEARISH",
                    False
                )
            )



            # =====================
            # BOS
            # =====================


            if bull_bos:

                bull_score += 40

                bull_reason.append(
                    "Bull BOS"
                )

                last_bull_bos = True

                last_bear_bos = False



            if bear_bos:

                bear_score += 40

                bear_reason.append(
                    "Bear BOS"
                )

                last_bear_bos = True

                last_bull_bos = False



            # =====================
            # CHOCH
            # =====================


            if bull_choch:

                bull_score += 30

                bull_reason.append(
                    "Bull CHOCH"
                )

                last_bull_choch = True



            if bear_choch:

                bear_score += 30

                bear_reason.append(
                    "Bear CHOCH"
                )

                last_bear_choch = True



            # =====================
            # EMA
            # =====================


            ema20 = row.get(
                "EMA20",
                0
            )

            ema50 = row.get(
                "EMA50",
                0
            )

            ema200 = row.get(
                "EMA200",
                0
            )


            if ema20 > ema50 > ema200:


                bull_score += 20

                bull_reason.append(
                    "EMA Bull"
                )



            elif ema20 < ema50 < ema200:


                bear_score += 20

                bear_reason.append(
                    "EMA Bear"
                )



            # =====================
            # New Event
            # =====================


            if (
                bull_score >= StructureEngine.BEAR_THRESHOLD
                and bull_score > bear_score
            ):


                current_structure = "BULL"

                current_score = min(
                    bull_score,
                    100
                )

                current_reason = ", ".join(
                    bull_reason
                )



            elif (
                bear_score >= StructureEngine.BULL_THRESHOLD
                and bear_score > bull_score
            ):


                current_structure = "BEAR"

                current_score = min(
                    bear_score,
                    100
                )

                current_reason = ", ".join(
                    bear_reason
                )



            else:


                if current_structure != "RANGE":

                    current_score = max(
                        current_score,
                        20
                    )



            idx = df.index[i]


            df.at[idx,"STRUCTURE"] = current_structure

            df.at[idx,"STRUCTURE_SCORE"] = current_score

            df.at[idx,"STRUCTURE_REASON"] = current_reason



            # حفظ BOS/CHOCH

            df.at[idx,"STRUCTURE_BULL_BOS"] = last_bull_bos

            df.at[idx,"STRUCTURE_BEAR_BOS"] = last_bear_bos

            df.at[idx,"STRUCTURE_BULL_CHOCH"] = last_bull_choch

            df.at[idx,"STRUCTURE_BEAR_CHOCH"] = last_bear_choch



        return df
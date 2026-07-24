from __future__ import annotations

import pandas as pd


class StructureEngine:
    """
    QuantCore Structure Engine V5

    Stateful Market Structure

    Logic:

        BOS:
            تغییر اصلی ساختار

        CHOCH:
            تغییر کاراکتر بازار

        EMA:
            تایید قدرت ساختار


    خروجی:

        STRUCTURE
        STRUCTURE_SCORE
        STRUCTURE_REASON


    رفتار:

        ساختار بعد از BOS حفظ می‌شود
        تا زمانی که BOS/CHOCH مخالف رخ دهد.

    """


    BOS_SCORE = 40
    CHOCH_SCORE = 30
    EMA_SCORE = 20



    @staticmethod
    def build(
        df: pd.DataFrame,
    ) -> pd.DataFrame:


        df = df.copy()


        df["STRUCTURE"] = "RANGE"

        df["STRUCTURE_SCORE"] = 0

        df["STRUCTURE_REASON"] = ""



        current_structure = "RANGE"

        current_score = 0

        current_reason = []



        for i in range(len(df)):


            row = df.iloc[i]



            # =================================
            # BOS CHANGE
            # =================================


            if bool(
                row.get(
                    "BULLISH_BOS",
                    False
                )
            ):


                current_structure = "BULL"

                current_score = StructureEngine.BOS_SCORE

                current_reason = [
                    "Bull BOS"
                ]



            elif bool(
                row.get(
                    "BEARISH_BOS",
                    False
                )
            ):


                current_structure = "BEAR"

                current_score = StructureEngine.BOS_SCORE

                current_reason = [
                    "Bear BOS"
                ]



            # =================================
            # CHOCH CHANGE
            # =================================


            if bool(
                row.get(
                    "CHOCH_BULLISH",
                    False
                )
            ):


                current_structure = "BULL"

                current_score = StructureEngine.CHOCH_SCORE

                current_reason = [
                    "Bull CHOCH"
                ]



            elif bool(
                row.get(
                    "CHOCH_BEARISH",
                    False
                )
            ):


                current_structure = "BEAR"

                current_score = StructureEngine.CHOCH_SCORE

                current_reason = [
                    "Bear CHOCH"
                ]



            # =================================
            # EMA CONFIRMATION
            # =================================


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



            score = current_score

            reasons = list(
                current_reason
            )



            if current_structure == "BULL":


                if ema20 > ema50 > ema200:


                    score += StructureEngine.EMA_SCORE

                    reasons.append(
                        "EMA Bull"
                    )



            elif current_structure == "BEAR":


                if ema20 < ema50 < ema200:


                    score += StructureEngine.EMA_SCORE

                    reasons.append(
                        "EMA Bear"
                    )



            # =================================
            # SAVE
            # =================================


            df.at[
                df.index[i],
                "STRUCTURE"
            ] = current_structure



            df.at[
                df.index[i],
                "STRUCTURE_SCORE"
            ] = min(
                score,
                100
            )



            df.at[
                df.index[i],
                "STRUCTURE_REASON"
            ] = ", ".join(
                reasons
            )



        return df
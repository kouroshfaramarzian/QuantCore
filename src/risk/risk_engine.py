from __future__ import annotations

import pandas as pd


class RiskEngine:

    DEFAULT_ATR_PERCENT = 0.002


    @staticmethod
    def calculate(
        df,
        signal,
        entry_price=None,
        rr=2,
        atr_multiplier=2,
        spread=0.0
    ):

        if df is None or df.empty:
            return RiskEngine.empty()


        last = df.iloc[-1]


        # -------------------------
        # Entry
        # -------------------------

        if entry_price is None:

            entry = float(
                last["close"]
            )

        else:

            entry = float(
                entry_price
            )


        # -------------------------
        # Spread
        # -------------------------

        if signal == "BUY":

            entry += spread / 2


        elif signal == "SELL":

            entry -= spread / 2



        # -------------------------
        # ATR Safe Handling
        # -------------------------

        atr_value = last.get(
            "ATR14",
            0
        )


        if pd.isna(atr_value):

            atr = 0.0

        else:

            atr = float(
                atr_value
            )



        if atr <= 0:

            atr = (
                entry *
                RiskEngine.DEFAULT_ATR_PERCENT
            )



        # -------------------------
        # Risk Calculation
        # -------------------------

        if signal == "BUY":


            stop_loss = (
                entry -
                atr * atr_multiplier
            )


            take_profit = (
                entry +
                (entry - stop_loss) *
                rr
            )



        elif signal == "SELL":


            stop_loss = (
                entry +
                atr * atr_multiplier
            )


            take_profit = (
                entry -
                (stop_loss - entry) *
                rr
            )


        else:

            return RiskEngine.empty()



        return {

            "entry":
                round(entry, 2),

            "stop_loss":
                round(stop_loss, 2),

            "take_profit":
                round(take_profit, 2),

            "risk":
                round(
                    abs(entry - stop_loss),
                    2
                )

        }



    @staticmethod
    def empty():

        return {

            "entry": None,

            "stop_loss": None,

            "take_profit": None,

            "risk": None

        }
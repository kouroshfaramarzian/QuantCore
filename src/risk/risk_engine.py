import pandas as pd


class RiskEngine:
    """
    QuantCore Risk Engine V2

    Logic:

    BUY:
        Entry = close
        SL = last swing low
        TP = risk * RR

    SELL:
        Entry = close
        SL = last swing high
        TP = risk * RR

    ATR used only as fallback.
    """


    @staticmethod
    def calculate(
        df: pd.DataFrame,
        signal: str,
        rr: float = 2.0,
        atr_multiplier: float = 2.0,
        buffer: float = 0.5,
    ) -> dict:


        if df is None or df.empty:

            return RiskEngine.empty()



        last = df.iloc[-1]


        entry = float(
            last["close"]
        )


        atr = float(
            last.get(
                "ATR14",
                0
            )
        )



        # =============================
        # BUY
        # =============================

        if signal == "BUY":


            swing_low = RiskEngine.get_last_swing_low(
                df
            )


            if swing_low is not None:


                stop_loss = (
                    swing_low
                    -
                    buffer
                )


            else:

                # ATR fallback

                stop_loss = (
                    entry
                    -
                    atr *
                    atr_multiplier
                )



            risk = entry - stop_loss



            if risk <= 0:

                return RiskEngine.empty()



            take_profit = (
                entry
                +
                risk *
                rr
            )



        # =============================
        # SELL
        # =============================

        elif signal == "SELL":


            swing_high = RiskEngine.get_last_swing_high(
                df
            )


            if swing_high is not None:


                stop_loss = (
                    swing_high
                    +
                    buffer
                )


            else:


                stop_loss = (
                    entry
                    +
                    atr *
                    atr_multiplier
                )



            risk = stop_loss - entry



            if risk <= 0:

                return RiskEngine.empty()



            take_profit = (
                entry
                -
                risk *
                rr
            )



        else:

            return RiskEngine.empty()



        return {

            "entry": round(
                entry,
                2
            ),

            "stop_loss": round(
                stop_loss,
                2
            ),

            "take_profit": round(
                take_profit,
                2
            ),

            "risk": round(
                risk,
                2
            ),

            "rr": rr

        }



    # =================================
    # SWING FINDERS
    # =================================


    @staticmethod
    def get_last_swing_low(df):


        if "SWING_LOW" not in df.columns:

            return None



        swings = df[
            df["SWING_LOW"] == True
        ]



        if swings.empty:

            return None



        return float(
            swings.iloc[-1]["low"]
        )




    @staticmethod
    def get_last_swing_high(df):


        if "SWING_HIGH" not in df.columns:

            return None



        swings = df[
            df["SWING_HIGH"] == True
        ]



        if swings.empty:

            return None



        return float(
            swings.iloc[-1]["high"]
        )




    @staticmethod
    def empty():

        return {

            "entry": None,

            "stop_loss": None,

            "take_profit": None,

            "risk": None

        }
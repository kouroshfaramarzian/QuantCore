class ConfirmationEngine:


    @staticmethod
    def confirm(df, signal):


        if df is None or df.empty:

            return False



        last = df.iloc[-1]



        structure = last.get(
            "STRUCTURE",
            "RANGE"
        )



        bullish_bos = bool(
            last.get(
                "BULLISH_BOS",
                False
            )
        )


        bearish_bos = bool(
            last.get(
                "BEARISH_BOS",
                False
            )
        )



        body = abs(

            float(
                last.get(
                    "BODY",
                    0
                )
            )

        )



        upper_wick = float(

            last.get(
                "UPPER_WICK",
                0
            )

        )



        lower_wick = float(

            last.get(
                "LOWER_WICK",
                0
            )

        )



        # ==========================
        # BUY CONFIRMATION
        # ==========================


        if signal == "BUY":


            if structure != "BULL":

                return False



            if not bullish_bos:

                return False



            # rejection candle

            if lower_wick < body:

                return False



            return True




        # ==========================
        # SELL CONFIRMATION
        # ==========================


        if signal == "SELL":


            if structure != "BEAR":

                return False



            if not bearish_bos:

                return False



            # rejection candle

            if upper_wick < body:

                return False



            return True




        return False
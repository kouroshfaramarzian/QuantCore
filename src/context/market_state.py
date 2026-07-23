class MarketStateResolver:
    """
    Combines all market information
    into one final market state.
    """

    @staticmethod
    def resolve(row):

        score_bull = 0
        score_bear = 0


        # =========================
        # STRUCTURE
        # =========================

        structure = row.get(
            "STRUCTURE",
            "RANGE"
        )


        if structure == "BULL":

            score_bull += 40


        elif structure == "BEAR":

            score_bear += 40



        # =========================
        # BOS
        # =========================

        if row.get(
            "BULLISH_BOS",
            False
        ):

            score_bull += 25


        if row.get(
            "BEARISH_BOS",
            False
        ):

            score_bear += 25



        # =========================
        # CHOCH
        # =========================

        if row.get(
            "CHOCH_BULLISH",
            False
        ):

            score_bull += 15


        if row.get(
            "CHOCH_BEARISH",
            False
        ):

            score_bear += 15



        # =========================
        # EMA
        # =========================

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


        if (
            ema20 >
            ema50 >
            ema200
        ):

            score_bull += 10


        elif (
            ema20 <
            ema50 <
            ema200
        ):

            score_bear += 10



        # =========================
        # FINAL STATE
        # =========================


        if score_bull >= score_bear + 20:

            return "BULL"


        if score_bear >= score_bull + 20:

            return "BEAR"


        return "RANGE"
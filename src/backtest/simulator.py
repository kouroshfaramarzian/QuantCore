class TradeSimulator:

    """
    Simulates SL / TP.
    """

    @staticmethod
    def update(

        candle,

        position,

    ):

        if position.direction == "BUY":

            if candle.low <= position.stop_loss:

                return "SL"

            if candle.high >= position.take_profit:

                return "TP"

        else:

            if candle.high >= position.stop_loss:

                return "SL"

            if candle.low <= position.take_profit:

                return "TP"

        return None
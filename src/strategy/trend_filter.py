class TrendFilter:
    """
    Filters trades using EMA trend.
    """

    @staticmethod
    def allow_buy(df):

        last = df.iloc[-1]

        return (

            last["EMA20"] >

            last["EMA50"] >

            last["EMA200"]

        )

    @staticmethod
    def allow_sell(df):

        last = df.iloc[-1]

        return (

            last["EMA20"] <

            last["EMA50"] <

            last["EMA200"]

        )
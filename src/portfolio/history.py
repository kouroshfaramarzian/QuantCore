class HistoryEngine:

    def __init__(self):

        self.trades = []

    def add(

        self,

        trade,

    ):

        self.trades.append(trade)

    def total_profit(self):

        return sum(

            trade.profit

            for trade in self.trades

        )

    def wins(self):

        return len(

            [

                t

                for t in self.trades

                if t.profit > 0

            ]

        )

    def losses(self):

        return len(

            [

                t

                for t in self.trades

                if t.profit <= 0

            ]

        )
from src.portfolio.metrics import PortfolioMetrics


class PortfolioEngine:

    def __init__(

        self,

        initial_balance: float,

    ):

        self.initial_balance = initial_balance

        self.balance = initial_balance

        self.metrics = PortfolioMetrics()

        self.positions = []

        self.closed_trades = []

    def add_position(

        self,

        position,

    ):

        self.positions.append(position)

    def close_trade(

        self,

        trade,

    ):

        self.closed_trades.append(trade)

        self.balance += trade.profit

        self.metrics.update(

            self.balance,

            trade,

        )

    @property
    def equity(self):

        floating = sum(

            p.floating_profit

            for p in self.positions

            if p.is_open

        )

        return self.balance + floating
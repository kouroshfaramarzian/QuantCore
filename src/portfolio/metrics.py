class PortfolioMetrics:

    def __init__(self):

        self.max_balance = 0

        self.max_drawdown = 0

        self.total_profit = 0

    def update(

        self,

        balance,

        trade,

    ):

        self.total_profit += trade.profit

        self.max_balance = max(

            self.max_balance,

            balance,

        )

        drawdown = self.max_balance - balance

        self.max_drawdown = max(

            self.max_drawdown,

            drawdown,

        )
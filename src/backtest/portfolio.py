class Portfolio:

    def __init__(

        self,

        initial_balance: float = 10000,

    ):

        self.initial_balance = initial_balance

        self.reset()

    def reset(self):

        self.balance = self.initial_balance

        self.equity = self.initial_balance

        self.max_balance = self.initial_balance

        self.max_drawdown = 0.0

        self.total_profit = 0.0

        self.total_loss = 0.0

        self.closed_trades = 0

    def update(

        self,

        trade,

    ):

        self.closed_trades += 1

        self.balance += trade.profit

        self.equity = self.balance

        if trade.profit >= 0:

            self.total_profit += trade.profit

        else:

            self.total_loss += abs(trade.profit)

        if self.balance > self.max_balance:

            self.max_balance = self.balance

        drawdown = self.max_balance - self.balance

        if drawdown > self.max_drawdown:

            self.max_drawdown = drawdown

    def summary(self):

        return {

            "initial_balance": round(self.initial_balance, 2),

            "balance": round(self.balance, 2),

            "equity": round(self.equity, 2),

            "closed_trades": self.closed_trades,

            "gross_profit": round(self.total_profit, 2),

            "gross_loss": round(self.total_loss, 2),

            "max_drawdown": round(self.max_drawdown, 2),

        }
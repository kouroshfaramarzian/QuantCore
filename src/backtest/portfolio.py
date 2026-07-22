class Portfolio:

    def __init__(

        self,

        initial_balance: float = 10000,

    ):

        self.initial_balance = initial_balance

        self.balance = initial_balance

        self.equity = initial_balance

        self.max_balance = initial_balance

        self.drawdown = 0

    def reset(self):

        self.balance = self.initial_balance

        self.equity = self.initial_balance

        self.max_balance = self.initial_balance

        self.drawdown = 0

    def update(

        self,

        trade,

    ):

        self.balance += trade.profit

        self.equity = self.balance

        self.max_balance = max(

            self.max_balance,

            self.balance,

        )

        current_dd = self.max_balance - self.balance

        self.drawdown = max(

            self.drawdown,

            current_dd,

        )
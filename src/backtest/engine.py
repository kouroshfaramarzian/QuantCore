from src.backtest.execution import ExecutionEngine
from src.backtest.portfolio import Portfolio
from src.backtest.statistics import Statistics


class TradingEngine:

    def __init__(self):

        self.execution = ExecutionEngine()

        self.portfolio = Portfolio()

        self.statistics = Statistics()

        self.position = None

        self.trades = []

    def reset(self):

        self.position = None

        self.trades.clear()

        self.portfolio.reset()

        self.statistics.reset()

    def open_position(

        self,

        position,

    ):

        self.position = position

    def close_position(

        self,

        exit_price,

        exit_time,

    ):

        trade = self.execution.execute(

            self.position,

            exit_price,

            exit_time,

        )

        self.trades.append(trade)

        self.statistics.update(trade)

        self.portfolio.update(trade)

        self.position = None

        return trade

    def report(self):

        return self.statistics.summary()
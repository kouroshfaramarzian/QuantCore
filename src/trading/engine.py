from src.trading.state import TradingState
from src.trading.session import TradingSession


class TradingEngine:

    def __init__(
        self,
        strategy,
        execution,
        portfolio,
        statistics,
    ):

        self.strategy = strategy
        self.execution = execution
        self.portfolio = portfolio
        self.statistics = statistics

        self.state = TradingState.STOPPED
        self.session = TradingSession()

    def start(self):

        self.state = TradingState.RUNNING
        self.session.start()

    def stop(self):

        self.session.stop()
        self.state = TradingState.STOPPED

    def process_tick(self, candle):

        if self.state != TradingState.RUNNING:
            return

        signal = self.strategy.generate_signal(candle)

        if signal is None:
            return

        trade = self.execution.execute(signal, candle)

        if trade is None:
            return

        self.portfolio.register(trade)

        self.statistics.register_trade(trade)

        self.session.register_trade()
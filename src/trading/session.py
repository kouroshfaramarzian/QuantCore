from datetime import datetime


class TradingSession:

    def __init__(self):

        self.started = None

        self.finished = None

        self.trades = 0

    def start(self):

        self.started = datetime.utcnow()

    def stop(self):

        self.finished = datetime.utcnow()

    def register_trade(self):

        self.trades += 1
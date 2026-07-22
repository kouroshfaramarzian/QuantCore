from datetime import datetime

from src.backtest.engine import TradingEngine
from src.backtest.position import Position


class Backtester:

    def __init__(self):

        self.engine = TradingEngine()

    def run(self, df):

        self.engine.reset()

        for i in range(1, len(df)):

            signal = df.iloc[i]["signal"]

            price = df.iloc[i]["close"]

            time = df.iloc[i].name

            if signal == "BUY" and not self.engine.position:

                position = Position(
                    symbol="XAUUSD",
                    direction="BUY",
                    volume=1.0,
                    entry_price=price,
                    stop_loss=0,
                    take_profit=0,
                    open_time=time,
                )

                self.engine.open_position(position)

            elif signal == "SELL" and self.engine.position:

                self.engine.close_position(
                    exit_price=price,
                    exit_time=time,
                )

        if self.engine.position:

            last_price = df.iloc[-1]["close"]

            last_time = df.iloc[-1].name

            self.engine.close_position(
                exit_price=last_price,
                exit_time=last_time,
            )

        return self.engine.trades

    def statistics(self):

        return self.engine.report()
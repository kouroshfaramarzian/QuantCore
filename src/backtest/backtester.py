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

            # ---------------- BUY ----------------

            if signal == "BUY":

                if self.engine.position is None:

                    self.engine.open_position(
                        Position(
                            symbol="XAUUSD",
                            direction="BUY",
                            volume=1.0,
                            entry_price=price,
                            stop_loss=0,
                            take_profit=0,
                            open_time=time,
                        )
                    )

                elif self.engine.position.direction == "SELL":

                    self.engine.close_position(price, time)

                    self.engine.open_position(
                        Position(
                            symbol="XAUUSD",
                            direction="BUY",
                            volume=1.0,
                            entry_price=price,
                            stop_loss=0,
                            take_profit=0,
                            open_time=time,
                        )
                    )

            # ---------------- SELL ----------------

            elif signal == "SELL":

                if self.engine.position is None:

                    self.engine.open_position(
                        Position(
                            symbol="XAUUSD",
                            direction="SELL",
                            volume=1.0,
                            entry_price=price,
                            stop_loss=0,
                            take_profit=0,
                            open_time=time,
                        )
                    )

                elif self.engine.position.direction == "BUY":

                    self.engine.close_position(price, time)

                    self.engine.open_position(
                        Position(
                            symbol="XAUUSD",
                            direction="SELL",
                            volume=1.0,
                            entry_price=price,
                            stop_loss=0,
                            take_profit=0,
                            open_time=time,
                        )
                    )

        if self.engine.position:

            self.engine.close_position(

                df.iloc[-1]["close"],

                df.iloc[-1].name,

            )

        return self.engine.trades

    def statistics(self):

        return self.engine.report()
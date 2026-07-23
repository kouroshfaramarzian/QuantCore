from src.backtest.engine import TradingEngine
from src.backtest.position import Position

from src.risk.risk_engine import RiskEngine


class Backtester:

    def __init__(self):

        self.engine = TradingEngine()

    def run(self, df):

        self.engine.reset()

        for i in range(1, len(df)):

            candle = df.iloc[i]

            signal = candle["signal"]

            high = candle["high"]

            low = candle["low"]

            close = candle["close"]

            time = candle.name

            # =====================================
            # CHECK OPEN POSITION
            # =====================================

            if self.engine.position is not None:

                pos = self.engine.position

                # ---------------- BUY ----------------

                if pos.direction == "BUY":

                    if low <= pos.stop_loss:

                        self.engine.close_position(

                            pos.stop_loss,

                            time,

                        )

                    elif high >= pos.take_profit:

                        self.engine.close_position(

                            pos.take_profit,

                            time,

                        )

                # ---------------- SELL ----------------

                elif pos.direction == "SELL":

                    if high >= pos.stop_loss:

                        self.engine.close_position(

                            pos.stop_loss,

                            time,

                        )

                    elif low <= pos.take_profit:

                        self.engine.close_position(

                            pos.take_profit,

                            time,

                        )

            # =====================================
            # OPEN NEW POSITION
            # =====================================

            if self.engine.position is None:

                if signal in ("BUY", "SELL"):

                    risk = RiskEngine.calculate(

                        df.iloc[: i + 1],

                        signal,

                    )

                    if risk["entry"] is None:

                        continue

                    position = Position(

                        symbol="XAUUSD",

                        direction=signal,

                        volume=1.0,

                        entry_price=risk["entry"],

                        stop_loss=risk["stop_loss"],

                        take_profit=risk["take_profit"],

                        open_time=time,

                    )

                    self.engine.open_position(position)

        # =====================================
        # CLOSE LAST POSITION
        # =====================================

        if self.engine.position is not None:

            self.engine.close_position(

                df.iloc[-1]["close"],

                df.iloc[-1].name,

            )

        return self.engine.trades

    def statistics(self):

        return self.engine.report()
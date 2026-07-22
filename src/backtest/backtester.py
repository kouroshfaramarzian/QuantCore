from datetime import datetime

from src.backtest.trade import Trade
from src.backtest.position import Position

from src.backtest.engine import BacktestEngine
from src.backtest.simulator import TradeSimulator

from src.strategy.signal_engine import SignalEngine
from src.risk.risk_engine import RiskEngine


class Backtester:
    """
    QuantCore Backtester v2
    """

    def __init__(self):

        self.engine = BacktestEngine()

        self.trades = []

    def run(self, df):

        self.trades = []

        for i in range(200, len(df)):

            history = df.iloc[: i + 1]

            candle = history.iloc[-1]

            # ===========================
            # Existing Position
            # ===========================

            if self.engine.has_position():

                position = self.engine.position

                result = TradeSimulator.update(

                    candle,

                    position,

                )

                if result:

                    self._close_trade(

                        candle,

                        position,

                        result,

                    )

                continue

            # ===========================
            # New Signal
            # ===========================

            signal = SignalEngine.generate(history)

            if signal["signal"].value == "HOLD":

                continue

            risk = RiskEngine.calculate(

                history,

                signal["signal"].value,

            )

            if risk["entry"] is None:

                continue

            position = Position(

                symbol="XAUUSD",

                direction=signal["signal"].value,

                entry_price=risk["entry"],

                stop_loss=risk["stop_loss"],

                take_profit=risk["take_profit"],

                volume=1.0,

                entry_time=candle.time,

            )

            self.engine.open_position(position)

        return self.trades

    def _close_trade(

        self,

        candle,

        position,

        result,

    ):

        trade = Trade(

            symbol=position.symbol,

            timeframe="M1",

            direction=position.direction,

            entry_time=position.entry_time,

            exit_time=candle.time,

            entry_price=position.entry_price,

            exit_price=candle.close,

            stop_loss=position.stop_loss,

            take_profit=position.take_profit,

            volume=position.volume,

            profit=self._profit(

                position,

                candle.close,

            ),

            rr=0,

            result=result,

        )

        self.trades.append(trade)

        self.engine.close_position()

    @staticmethod
    def _profit(

        position,

        exit_price,

    ):

        if position.direction == "BUY":

            return exit_price - position.entry_price

        return position.entry_price - exit_price
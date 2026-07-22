from datetime import datetime

from src.backtest.trade import Trade


class ExecutionEngine:

    def execute(

        self,

        position,

        exit_price: float,

        exit_time: datetime,

    ) -> Trade:

        position.close(

            exit_price,

            exit_time,

        )

        if position.direction == "BUY":

            profit = exit_price - position.entry_price

        else:

            profit = position.entry_price - exit_price

        return Trade(

            symbol=position.symbol,

            timeframe="",

            direction=position.direction,

            entry_time=position.open_time,

            exit_time=exit_time,

            entry_price=position.entry_price,

            exit_price=exit_price,

            stop_loss=position.stop_loss,

            take_profit=position.take_profit,

            volume=position.volume,

            profit=profit,

            rr=0,

            result="WIN" if profit > 0 else "LOSS",

        )
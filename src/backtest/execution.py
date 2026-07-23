from datetime import datetime

from src.backtest.trade import Trade


class ExecutionEngine:

    SPREAD = 0.20
    COMMISSION = 0.00
    POINT = 0.01

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

            gross_profit = exit_price - position.entry_price

        else:

            gross_profit = position.entry_price - exit_price

        gross_profit -= self.SPREAD
        gross_profit -= self.COMMISSION

        pips = gross_profit / self.POINT

        if gross_profit > 0:

            result = "WIN"

        elif gross_profit < 0:

            result = "LOSS"

        else:

            result = "BE"

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

            profit=gross_profit,

            pips=pips,
            
            rr=0,

            result=result,

        )
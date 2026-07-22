from datetime import datetime

from src.domain.trade import Trade
from src.domain.position import Position
from src.domain.enums import TradeResult


class TradeLifecycle:

    def close(

        self,

        position: Position,

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

            result=TradeResult.WIN if profit > 0 else TradeResult.LOSS,

        )
from datetime import datetime

from src.domain.order import Order


class OrderFactory:

    def create(

        self,

        signal,

        risk,

        symbol,

        volume,

    ):

        return Order(

            symbol=symbol,

            direction=signal.signal.value,

            volume=volume,

            price=risk.entry,

            stop_loss=risk.stop_loss,

            take_profit=risk.take_profit,

            time=datetime.now(),

        )
from src.execution.order import Order
from src.execution.position import Position


class OrderManager:
    """
    Converts executable orders into positions.
    """

    @staticmethod
    def execute(
        order: Order,
    ) -> Position:

        return Position(

            symbol=order.symbol,

            direction=order.direction,

            volume=order.volume,

            entry_price=order.entry_price,

            stop_loss=order.stop_loss,

            take_profit=order.take_profit,

            open_time=order.open_time,

        )
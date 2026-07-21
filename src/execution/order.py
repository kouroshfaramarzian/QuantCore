from dataclasses import dataclass
from datetime import datetime


@dataclass
class Order:
    """
    Represents a market order.
    """

    symbol: str

    direction: str

    volume: float

    entry_price: float

    stop_loss: float

    take_profit: float

    open_time: datetime

    status: str = "OPEN"
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Position:
    """
    Represents an active position.
    """

    symbol: str

    direction: str

    volume: float

    entry_price: float

    stop_loss: float

    take_profit: float

    open_time: datetime

    is_open: bool = True

    close_time: datetime | None = None

    close_price: float | None = None
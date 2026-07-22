from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Position:
    """
    Represents one open position.
    """

    symbol: str

    direction: str

    volume: float

    entry_price: float

    stop_loss: float

    take_profit: float

    open_time: datetime

    is_open: bool = True

    close_time: Optional[datetime] = None

    close_price: Optional[float] = None

    def close(
        self,
        price: float,
        time: datetime,
    ):

        self.close_price = price

        self.close_time = time

        self.is_open = False
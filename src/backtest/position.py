from dataclasses import dataclass

from datetime import datetime


@dataclass
class Position:

    symbol: str

    direction: str

    entry_price: float

    stop_loss: float

    take_profit: float

    volume: float

    entry_time: datetime

    is_open: bool = True
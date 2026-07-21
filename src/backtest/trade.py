from dataclasses import dataclass
from datetime import datetime


@dataclass
class Trade:
    """
    Represents one completed trade.
    """

    symbol: str

    timeframe: str

    direction: str

    entry_time: datetime

    exit_time: datetime

    entry_price: float

    exit_price: float

    stop_loss: float

    take_profit: float

    volume: float

    profit: float

    rr: float

    result: str
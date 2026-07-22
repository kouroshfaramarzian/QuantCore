from dataclasses import dataclass
from datetime import datetime


@dataclass
class Order:

    symbol: str

    direction: str

    volume: float

    price: float

    stop_loss: float

    take_profit: float

    time: datetime
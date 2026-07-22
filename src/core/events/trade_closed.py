from dataclasses import dataclass
from datetime import datetime

from src.domain.trade import Trade


@dataclass(slots=True)
class TradeClosedEvent:

    timestamp: datetime

    trade: Trade
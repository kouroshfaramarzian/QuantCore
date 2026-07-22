from dataclasses import dataclass, field

from src.domain.position import Position


@dataclass(slots=True)
class Portfolio:

    positions: list[Position] = field(default_factory=list)

    closed_profit: float = 0.0

    floating_profit: float = 0.0

    drawdown: float = 0.0
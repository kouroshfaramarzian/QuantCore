from dataclasses import dataclass


@dataclass(slots=True)
class Market:

    symbol: str

    timeframe: str

    spread: float

    commission: float

    slippage: float
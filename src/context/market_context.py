from dataclasses import dataclass


@dataclass
class MarketContext:
    """
    Represents the current market state.
    """

    trend: str

    momentum: str

    volatility: str

    session: str
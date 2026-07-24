from dataclasses import dataclass
from typing import Optional


@dataclass
class MarketContext:
    """
    QuantCore Market Context

    خروجی نهایی ContextEngine
    """

    trend: str

    momentum: str

    volatility: str

    session: str

    # Debug information

    confidence: Optional[str] = None

    source: Optional[str] = None
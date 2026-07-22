from dataclasses import dataclass

from src.domain.enums import Signal


@dataclass(slots=True)
class SignalDecision:

    signal: Signal

    buy_score: float

    sell_score: float

    confidence: float
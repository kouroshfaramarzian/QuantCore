from dataclasses import dataclass

from src.domain.signal import SignalDecision
from src.domain.risk import RiskDecision


@dataclass(slots=True)
class StrategyDecision:

    signal: SignalDecision

    risk: RiskDecision
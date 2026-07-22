from dataclasses import dataclass


@dataclass(slots=True)
class RiskDecision:

    entry: float | None

    stop_loss: float | None

    take_profit: float | None

    volume: float

    risk_percent: float

    rr: float
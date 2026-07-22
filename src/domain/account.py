from dataclasses import dataclass


@dataclass(slots=True)
class Account:

    balance: float

    equity: float

    margin: float

    free_margin: float

    leverage: int
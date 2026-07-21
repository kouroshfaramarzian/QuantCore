from enum import Enum


class Signal(Enum):
    """
    Trading signals.
    """

    BUY = "BUY"

    SELL = "SELL"

    HOLD = "HOLD"

    EXIT_BUY = "EXIT BUY"

    EXIT_SELL = "EXIT SELL"
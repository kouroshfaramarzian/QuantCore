from enum import Enum


class Direction(Enum):

    BUY = "BUY"

    SELL = "SELL"


class Signal(Enum):

    BUY = "BUY"

    SELL = "SELL"

    HOLD = "HOLD"


class TradeResult(Enum):

    WIN = "WIN"

    LOSS = "LOSS"

    BREAKEVEN = "BREAKEVEN"
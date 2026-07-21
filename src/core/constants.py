"""
Global constants for QuantCore.
These values are fixed and should never be hardcoded
throughout the project.
"""


class DatasetColumns:
    TIME = "time"
    OPEN = "open"
    HIGH = "high"
    LOW = "low"
    CLOSE = "close"
    TICK_VOLUME = "tick_volume"
    SPREAD = "spread"
    REAL_VOLUME = "real_volume"


class PredictionLabels:
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


class FileExtensions:
    CSV = ".csv"
    PARQUET = ".parquet"
    PKL = ".pkl"
    JSON = ".json"


class Timeframes:
    M1 = "M1"
    M5 = "M5"
    M15 = "M15"
    H1 = "H1"
    H4 = "H4"
    D1 = "D1"


class Markets:
    XAUUSD = "XAUUSD"
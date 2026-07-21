from dataclasses import dataclass

from src.core.paths import (
    DATASETS_DIR,
    MODELS_DIR,
    LOGS_DIR,
)


@dataclass(frozen=True)
class ProjectConfig:
    # -------------------------
    # Project
    # -------------------------
    NAME: str = "QuantCore"
    VERSION: str = "0.1.0"
    DEBUG: bool = True

    # -------------------------
    # Market
    # -------------------------
    SYMBOL: str = "XAUUSD"
    TIMEFRAME: str = "M1"
    HISTORY_SIZE: int = 1000

    # -------------------------
    # Dataset
    # -------------------------
    TRAIN_RATIO: float = 0.70
    VALID_RATIO: float = 0.15
    TEST_RATIO: float = 0.15

    # -------------------------
    # Paths
    # -------------------------
    DATASETS_DIR = DATASETS_DIR
    MODELS_DIR = MODELS_DIR
    LOGS_DIR = LOGS_DIR


config = ProjectConfig()
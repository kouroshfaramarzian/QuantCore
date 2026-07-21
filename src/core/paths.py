from pathlib import Path

# Project Root
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# Main Directories
CONFIG_DIR = ROOT_DIR / "config"
DATASETS_DIR = ROOT_DIR / "datasets"
MODELS_DIR = ROOT_DIR / "models"
LOGS_DIR = ROOT_DIR / "logs"
TESTS_DIR = ROOT_DIR / "tests"
SRC_DIR = ROOT_DIR / "src"

# Automatically create required directories
for directory in [
    CONFIG_DIR,
    DATASETS_DIR,
    MODELS_DIR,
    LOGS_DIR,
    TESTS_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)
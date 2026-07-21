import logging
from pathlib import Path

from src.core.config import config

# Log file
log_file = config.LOGS_DIR / "quantcore.log"

# Logger
logger = logging.getLogger("QuantCore")

# جلوگیری از ساخت Handler تکراری
if not logger.handlers:

    logger.setLevel(logging.INFO)

    # Console
    console_handler = logging.StreamHandler()

    # File
    file_handler = logging.FileHandler(log_file, encoding="utf-8")

    # Format
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s | %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
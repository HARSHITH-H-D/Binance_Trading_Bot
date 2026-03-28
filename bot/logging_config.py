
import logging
import os

def setup_logger(name: str = "trading_bot") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Avoid duplicate handlers if called multiple times
    if logger.handlers:
        return logger

    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)

    # File handler — logs everything to file
    file_handler = logging.FileHandler("logs/trading_bot.log")
    file_handler.setLevel(logging.DEBUG)

    # Console handler — shows INFO and above
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Format
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
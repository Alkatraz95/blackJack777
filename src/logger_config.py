import logging
from pathlib import Path


def get_module_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Логи будут в корне проекта: logs/utils.log и logs/masks.log
    log_path = Path("logs") / f"{name}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # mode='w' — перезапись при каждом запуске (требование задания)
    file_handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger

import datetime
from typing import Optional
import logging

try:
    from .logger_config import get_module_logger

    logger = get_module_logger("utils")
except ImportError:
    # Если logger_config нет, создаём простой логгер в консоль
    logger = logging.getLogger("utils")
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)


def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    """
    Конвертирует сумму из одной валюты в другую.

    Для домашнего задания используем фиксированные курсы, чтобы тесты были стабильными.
    Результат округляется до 2 знаков после запятой.
    """

    rates = {
        "USD": 1.0,
        "EUR": 0.85,
        "RUB": 90.0,
        "BYN": 2.5,
    }

    if from_currency not in rates or to_currency not in rates:
        logger.error("Неизвестный код валюты: %s или %s", from_currency, to_currency)
        raise ValueError(f"Неизвестный код валюты: {from_currency} или {to_currency}")

    # Конвертация через USD как промежуточную валюту
    amount_in_usd = amount / rates[from_currency]
    result = amount_in_usd * rates[to_currency]

    logger.info(
        "Конвертация: %.2f %s → %.2f %s (курс: %.4f)",
        amount,
        from_currency,
        result,
        to_currency,
        rates[to_currency],
    )

    # Округляем до 2 знаков, как и было задумано
    return round(result, 2)


def log_execution(func):
    """Декоратор для логирования времени выполнения функции."""

    def wrapper(*args, **kwargs):
        start_time = datetime.datetime.now()
        logger.debug("[%s] Начало выполнения: %s", start_time, func.__name__)
        try:
            result = func(*args, **kwargs)
            end_time = datetime.datetime.now()
            duration = (end_time - start_time).total_seconds()
            logger.debug(
                "[%s] Завершено: %s, длительность: %.3f сек",
                end_time,
                func.__name__,
                duration,
            )
            return result
        except Exception as e:
            end_time = datetime.datetime.now()
            logger.exception("[%s] Ошибка в %s: %s", end_time, func.__name__, e)
            raise

    return wrapper

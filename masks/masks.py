from src.logger_config import get_module_logger


# Инициализируем логгер для модуля masks
logger = get_module_logger("masks")


def apply_mask(data):
    """
    Применяет маску к данным.

    В текущей реализации просто логирует вызов и возвращает данные без изменений.
    Сюда позже можно добавить реальную логику маскирования.
    """
    logger.debug("Применяем маску в masks.py. Данные: %s", data)
    return data


def mask_card_number(card_number: str) -> str:
    """
    Маскирует номер карты, оставляя первые 4 и последние 4 цифры открытыми.
    Пример: '7000792289606361' -> '7000 79** **** 6361'

    :param card_number: Номер карты в виде строки (только цифры)
    :return: Маскированный номер
    :raises ValueError: Если номер не состоит из 16 цифр
    """
    if not card_number or not card_number.isdigit():
        raise ValueError("Номер карты должен состоять только из цифр.")

    if len(card_number) != 16:
        raise ValueError(f"Номер карты должен состоять из 16 цифр, получено: {len(card_number)}")

    masked = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    logger.info("Замаскирован номер карты: %s -> %s", card_number, masked)
    return masked


def mask_account_number(account_number: str) -> str:
    """
    Маскирует номер счёта, оставляя только последние 4 цифры.
    Пример: '12345678901234567890' -> '**7890'

    :param account_number: Номер счёта в виде строки
    :return: Маскированный номер счёта
    :raises ValueError: Если номер слишком короткий
    """
    if not account_number or len(account_number) < 4:
        raise ValueError("Номер счёта должен содержать минимум 4 цифры.")

    masked = "**" + account_number[-4:]
    logger.info("Замаскирован номер счёта: %s -> %s", account_number, masked)
    return masked

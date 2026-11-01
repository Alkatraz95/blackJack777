from datetime import datetime

from .masks import get_mask_account
from .masks import get_mask_card_number


def mask_account_card(pay_info: str) -> str:
    """Обрабатывает информацию о картах и счетах и возвращает строку с замаскированным номером"""
    if not isinstance(pay_info, str) or not pay_info.strip():
        raise ValueError("Некорректный формат данных: ожидается непустая строка.")

    parts = pay_info.split()
    if len(parts) < 2:
        raise ValueError("Строка не содержит нужной информации для обработки")

    account = "Счет"
    number = parts[-1]

    try:
        if parts[0] == account:
            return get_mask_account(number)
        return get_mask_card_number(number)
    except ValueError as e:
        # Перехватываем ошибки из внутренних функций
        raise ValueError(f"Ошибка обработки номера: {str(e)}")


def get_date(date_string: str) -> str:
    """Смена даты с формата ISO на 'ДД.ММ.ГГГГ'"""
    date = datetime.fromisoformat(date_string)
    formatted_date = date.strftime("%d.%m.%Y")
    return formatted_date
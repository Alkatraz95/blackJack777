"""Поиск транзакций по строке в описании с помощью re."""

import re
from typing import Any


def process_bank_search(data: list[dict[str, Any]], search: str) -> list[dict[str, Any]]:
    """Возвращает транзакции, у которых в поле description есть заданная строка.

    Поиск выполняется без учёта регистра. Спецсимволы экранируются через re.escape.

    Args:
        data: список словарей с транзакциями.
        search: строка для поиска.

    Returns:
        Список словарей с подходящими транзакциями.
    """
    if not search:
        return []
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    return [t for t in data if pattern.search(str(t.get("description", "")))]

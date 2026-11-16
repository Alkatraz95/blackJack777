"""Подсчёт операций по категориям через collections.Counter."""

from collections import Counter
from typing import Any


def process_bank_operations(data: list[dict[str, Any]], categories: list[str]) -> dict[str, int]:
    """Подсчитывает количество операций для заданных категорий.

    Категория определяется по полю description: если строка категории
    присутствует в description, операция относится к этой категории.

    Args:
        data: список словарей с транзакциями.
        categories: список названий категорий для подсчёта.

    Returns:
        Словарь {категория: количество}.
    """
    found = []
    for t in data:
        desc = str(t.get("description", ""))
        for cat in categories:
            if cat in desc:
                found.append(cat)
                break
    return dict(Counter(found))

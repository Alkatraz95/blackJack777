"""Тесты для process_bank_operations."""

from src.categories import process_bank_operations


DATA = [
    {"id": "1", "description": "Супермаркеты Магнит", "state": "EXECUTED"},
    {"id": "2", "description": "Каршеринг Ситидрайв", "state": "EXECUTED"},
    {"id": "3", "description": "Супермаркеты Дикси", "state": "CANCELED"},
]


def test_process_bank_operations():
    result = process_bank_operations(DATA, ["Супермаркеты", "Каршеринг"])
    assert result == {"Супермаркеты": 2, "Каршеринг": 1}


def test_process_bank_operations_empty():
    result = process_bank_operations([], ["Супермаркеты"])
    assert result == {}


def test_process_bank_operations_no_match():
    result = process_bank_operations(DATA, ["Кафе"])
    assert result == {}

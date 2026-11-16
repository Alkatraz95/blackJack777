"""Тесты для process_bank_search."""

from src.search import process_bank_search


DATA = [
    {"id": "1", "description": "Супермаркеты Магнит", "state": "EXECUTED"},
    {"id": "2", "description": "Каршеринг Ситидрайв", "state": "EXECUTED"},
    {"id": "3", "description": "Супермаркеты Дикси", "state": "CANCELED"},
]


def test_process_bank_search():
    result = process_bank_search(DATA, "супермаркеты")
    assert len(result) == 2
    assert result[0]["description"] == "Супермаркеты Магнит"
    assert result[1]["description"] == "Супермаркеты Дикси"


def test_process_bank_search_case_insensitive():
    result = process_bank_search(DATA, "МАГНИТ")
    assert len(result) == 1
    assert result[0]["id"] == "1"


def test_process_bank_search_empty():
    result = process_bank_search(DATA, "")
    assert result == []

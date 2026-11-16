"""Тест для main (формальное покрытие пункта про UI)."""

from unittest.mock import patch


@patch("src.main.read_transactions_from_csv")
@patch("builtins.input")
def test_main_does_not_crash(mock_input, mock_read):
    mock_read.return_value = [{"id": "1", "description": "Покупка", "state": "EXECUTED"}]
    mock_input.side_effect = [
        "2",          # пункт 2 (CSV)
        "data.csv",   # путь
        "EXECUTED",   # статус
        "нет",        # сортировка
        "да",         # только RUB
        "нет",        # поиск
    ]
    from src.main import main

    main()   # главная цель — без исключений

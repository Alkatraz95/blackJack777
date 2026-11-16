"""Тесты функций считывания транзакций из CSV и Excel."""

from unittest.mock import mock_open, patch

import pandas as pd

from src.readers import (
    read_transactions_from_csv,
    read_transactions_from_excel,
)

CSV_DATA = (
    'id;state;date;amount;currency_name;currency_code;from;to;description\n'
    '650703;EXECUTED;2023-09-05T11:30:32Z;16210;Sol;PEN;'
    'Счет 58803664561298323391;Счет 39745660563456619397;Перевод организации\n'
    ';;;;;;;\n'
)


@patch('builtins.open', mock_open(read_data=CSV_DATA))
def test_read_transactions_from_csv():
    """Проверяет чтение CSV: корректные строки возвращаются, пустые отбрасываются."""
    result = read_transactions_from_csv('fake.csv')
    assert len(result) == 1
    assert result[0]['id'] == '650703'
    assert result[0]['state'] == 'EXECUTED'
    assert result[0]['amount'] == '16210'
    assert result[0]['description'] == 'Перевод организации'


@patch('builtins.open', mock_open(read_data='id;state\n'))
def test_read_transactions_from_csv_empty():
    """Проверяет чтение CSV без строк данных: возвращается пустой список."""
    result = read_transactions_from_csv('fake.csv')
    assert result == []


@patch('src.readers.pd.read_excel')
def test_read_transactions_from_excel(mock_read):
    """Проверяет чтение Excel: read_excel вызывается и результат — список словарей."""
    mock_read.return_value = pd.DataFrame({
        'id': [650703],
        'state': ['EXECUTED'],
        'amount': [16210],
        'description': ['Перевод организации'],
    })
    result = read_transactions_from_excel('fake.xlsx')
    assert result == [{'id': 650703, 'state': 'EXECUTED',
                       'amount': 16210, 'description': 'Перевод организации'}]
    mock_read.assert_called_once_with('fake.xlsx', engine='openpyxl')

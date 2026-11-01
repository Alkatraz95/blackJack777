from unittest.mock import mock_open, patch

import requests

from src.currency import get_transaction_amount_in_rub
from src.utils import read_transactions

# ---------- Чтение JSON: реальные временные файлы (tmp_path) ----------


def test_valid_json(tmp_path):
    """Тест: корректный JSON со списком словарей"""
    file = tmp_path / "operations.json"
    file.write_text('[{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]')
    result = read_transactions(str(file))
    expected = [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]
    assert result == expected


def test_file_not_found():
    """Тест: файл не существует — должен вернуть пустой список"""
    result = read_transactions("nonexistent.json")
    assert result == []


def test_invalid_json(tmp_path):
    """Тест: содержимое не JSON — должен вернуть пустой список"""
    file = tmp_path / "bad.json"
    file.write_text("not a json string at all")
    result = read_transactions(str(file))
    assert result == []


def test_not_list(tmp_path):
    """Тест: JSON есть, но это объект, не список — должен вернуть пустой список"""
    file = tmp_path / "not_list.json"
    file.write_text('{"id": 1}')
    result = read_transactions(str(file))
    assert result == []


def test_empty_file(tmp_path):
    """Тест: пустой файл — должен вернуть пустой список"""
    file = tmp_path / "empty.json"
    file.write_text("")
    result = read_transactions(str(file))
    assert result == []


def test_mixed_data(tmp_path):
    """Тест: в списке разные типы данных — должны остаться только словари"""
    file = tmp_path / "mixed.json"
    file.write_text('[{"amount": 100}, "string", null, 123, {"amount": 200}]')
    result = read_transactions(str(file))
    assert len(result) == 2
    assert result[0]["amount"] == 100
    assert result[1]["amount"] == 200


def test_json_with_bom(tmp_path):
    """Тест: файл с BOM — читается без ошибок благодаря utf-8-sig"""
    file = tmp_path / "bom.json"
    file.write_bytes(b'\xef\xbb\xbf[{"id": 1, "amount": 100}]')
    result = read_transactions(str(file))
    assert result == [{"id": 1, "amount": 100}]


# ---------- Чтение JSON: mock + patch (как требует задание) ----------


@patch("builtins.open", new_callable=mock_open, read_data='[{"id": 1, "amount": 100}]')
def test_read_with_mock(mock_file):
    """Тест: мокает встроенный open — реальный файл не создаётся"""
    result = read_transactions("fake/path.json")
    assert result == [{"id": 1, "amount": 100}]
    mock_file.assert_called_once_with("fake/path.json", "r", encoding="utf-8-sig")


@patch("builtins.open", new_callable=mock_open, read_data="not json")
def test_read_mock_invalid_json(mock_file):
    """Тест: mock возвращает не-JSON — функция возвращает пустой список"""
    assert read_transactions("fake/path.json") == []


@patch("builtins.open", side_effect=FileNotFoundError)
def test_read_mock_file_not_found(mock_file):
    """Тест: mock имитирует отсутствие файла — пустой список"""
    assert read_transactions("fake/path.json") == []


# ---------- Конвертация валюты: mock + patch ----------


@patch("src.currency.requests.get")
def test_convert_usd_transaction(mock_get):
    """Тест: транзакция в USD конвертируется в рубли через API (замокан)"""
    mock_get.return_value.json.return_value = {"result": 9000.0}
    transaction = {"id": 1, "amount": 100, "currency": "USD"}
    result = get_transaction_amount_in_rub(transaction)
    assert result == 9000.0
    mock_get.assert_called_once()


@patch("src.currency.requests.get")
def test_convert_eur_transaction(mock_get):
    """Тест: транзакция в EUR конвертируется в рубли через API (замокан)"""
    mock_get.return_value.json.return_value = {"result": 10000.0}
    transaction = {"id": 2, "amount": 100, "currency": "EUR"}
    assert get_transaction_amount_in_rub(transaction) == 10000.0


def test_convert_rub_no_api_call():
    """Тест: транзакция в RUB — API не вызывается, сумма без конвертации"""
    transaction = {"id": 3, "amount": 500, "currency": "RUB"}
    assert get_transaction_amount_in_rub(transaction) == 500.0


def test_convert_missing_fields():
    """Тест: нет amount и currency — возвращается 0.0 без обращения к API"""
    assert get_transaction_amount_in_rub({}) == 0.0


@patch("src.currency.requests.get", side_effect=requests.ConnectionError("нет сети"))
def test_convert_api_error_returns_amount(mock_get):
    """Тест: API недоступен — возвращается исходная сумма без падения"""
    transaction = {"id": 4, "amount": 100, "currency": "USD"}
    assert get_transaction_amount_in_rub(transaction) == 100.0

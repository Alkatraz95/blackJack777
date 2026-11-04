"""Тесты утилит чтения файла и конвертации."""

import json
import os
from unittest.mock import patch

import pytest

from src.utils import convert_transaction_to_rub, read_json_file


# --- read_json_file ---

def test_read_json_file_valid(tmp_path):
    file = tmp_path / "operations.json"
    file.write_text(json.dumps([{"id": 1, "state": "EXECUTED"}]), encoding="utf-8")
    assert read_json_file(str(file)) == [{"id": 1, "state": "EXECUTED"}]


def test_read_json_file_not_found():
    assert read_json_file("no_such_file.json") == []


def test_read_json_file_invalid_json(tmp_path):
    file = tmp_path / "bad.json"
    file.write_text("{не json}", encoding="utf-8")
    assert read_json_file(str(file)) == []


def test_read_json_file_empty(tmp_path):
    file = tmp_path / "empty.json"
    file.write_text("[]", encoding="utf-8")
    assert read_json_file(str(file)) == []


def test_read_json_file_not_a_list(tmp_path):
    file = tmp_path / "dict.json"
    file.write_text('{"key": "value"}', encoding="utf-8")
    assert read_json_file(str(file)) == []


# --- convert_transaction_to_rub ---

def test_convert_rub_no_api_call():
    transaction = {
        "operationAmount": {
            "amount": "1000.0",
            "currency": {"name": "руб.", "code": "RUB"},
        }
    }
    with patch("src.utils.requests.get") as mock_get:
        assert convert_transaction_to_rub(transaction) == 1000.0
        mock_get.assert_not_called()


@patch.dict(os.environ, {"API_KEY": "test-key"})
@patch("src.utils.requests.get")
def test_convert_usd(mock_get):
    mock_get.return_value.json.return_value = {"rates": {"RUB": 90.0}}
    mock_get.return_value.status_code = 200

    transaction = {
        "operationAmount": {
            "amount": "100.0",
            "currency": {"name": "USD", "code": "USD"},
        }
    }
    assert convert_transaction_to_rub(transaction) == 9000.0
    mock_get.assert_called_once()


@patch.dict(os.environ, {"API_KEY": "test-key"})
@patch("src.utils.requests.get")
def test_convert_eur(mock_get):
    mock_get.return_value.json.return_value = {"rates": {"RUB": 100.0}}
    mock_get.return_value.status_code = 200

    transaction = {
        "operationAmount": {
            "amount": "50.0",
            "currency": {"name": "EUR", "code": "EUR"},
        }
    }
    assert convert_transaction_to_rub(transaction) == 5000.0


def test_convert_unsupported_currency():
    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {"name": "GBP", "code": "GBP"},
        }
    }
    with pytest.raises(ValueError):
        convert_transaction_to_rub(transaction)

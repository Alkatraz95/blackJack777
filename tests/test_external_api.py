"""Тесты конвертации валют."""

import os
from unittest.mock import patch

import pytest

from src.external_api import convert_to_rub


def test_convert_rub_transaction():
    transaction = {
        "operationAmount": {
            "amount": "31957.58",
            "currency": {"name": "руб.", "code": "RUB"},
        }
    }
    assert convert_to_rub(transaction) == 31957.58


@patch.dict(os.environ, {"API_KEY": "test-key"})
@patch("src.utils.requests.get")
def test_convert_usd_transaction(mock_get):
    mock_get.return_value.json.return_value = {"rates": {"RUB": 90.0}}
    mock_get.return_value.status_code = 200

    transaction = {
        "operationAmount": {
            "amount": "100.0",
            "currency": {"name": "USD", "code": "USD"},
        }
    }
    assert convert_to_rub(transaction) == 9000.0
    mock_get.assert_called_once()


@patch.dict(os.environ, {"API_KEY": "test-key"})
@patch("src.utils.requests.get")
def test_convert_eur_transaction(mock_get):
    mock_get.return_value.json.return_value = {"rates": {"RUB": 100.0}}
    mock_get.return_value.status_code = 200

    transaction = {
        "operationAmount": {
            "amount": "50.0",
            "currency": {"name": "EUR", "code": "EUR"},
        }
    }
    assert convert_to_rub(transaction) == 5000.0


def test_missing_currency_raises():
    with pytest.raises(ValueError):
        convert_to_rub({"operationAmount": {"amount": "100"}})


def test_unsupported_currency_raises():
    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {"name": "GBP", "code": "GBP"},
        }
    }
    with pytest.raises(ValueError):
        convert_to_rub(transaction)


def test_no_api_key_raises():
    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {"name": "USD", "code": "USD"},
        }
    }
    env = {k: v for k, v in os.environ.items() if k != "API_KEY"}
    with patch.dict(os.environ, env, clear=True):
        with pytest.raises(ValueError):
            convert_to_rub(transaction)

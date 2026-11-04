import json
from unittest.mock import MagicMock, mock_open, patch

import pytest

from src.utils import convert_transaction_to_rub, read_json_file


# --- Тесты для read_json_file ---

def test_read_json_file_valid():
    content = json.dumps([{"id": 1, "amount": 100.0, "currency": "RUB"}])
    with patch("builtins.open", mock_open(read_data=content)):
        assert read_json_file("data/operations.json") == [
            {"id": 1, "amount": 100.0, "currency": "RUB"}
        ]


def test_read_json_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        assert read_json_file("no_such_file.json") == []


def test_read_json_file_invalid_json():
    with patch("builtins.open", mock_open(read_data="{not valid")):
        assert read_json_file("data/operations.json") == []


def test_read_json_file_empty():
    with patch("builtins.open", mock_open(read_data="")):
        assert read_json_file("data/operations.json") == []


def test_read_json_file_not_a_list():
    with patch("builtins.open", mock_open(read_data='{"id": 1}')):
        assert read_json_file("data/operations.json") == []


# --- Тесты для convert_transaction_to_rub ---

def test_convert_rub_no_api_call():
    transaction = {"amount": 1000.0, "currency": "RUB"}
    with patch("src.utils.requests.get") as mock_get:
        result = convert_transaction_to_rub(transaction)
        assert result == 1000.0
        mock_get.assert_not_called()


def test_convert_usd():
    transaction = {"amount": 100.0, "currency": "USD"}
    mock_response = MagicMock()
    mock_response.json.return_value = {"result": 9000.5}

    with patch("src.utils.requests.get", return_value=mock_response) as mock_get:
        result = convert_transaction_to_rub(transaction)

    assert result == 9000.5
    mock_get.assert_called_once()
    args, kwargs = mock_get.call_args
    assert kwargs["headers"]["apikey"]
    mock_response.raise_for_status.assert_called_once()


def test_convert_eur():
    transaction = {"amount": 50.0, "currency": "EUR"}
    mock_response = MagicMock()
    mock_response.json.return_value = {"result": 5000.0}

    with patch("src.utils.requests.get", return_value=mock_response):
        result = convert_transaction_to_rub(transaction)

    assert result == 5000.0


def test_convert_unsupported_currency():
    transaction = {"amount": 100.0, "currency": "GBP"}
    with pytest.raises(ValueError):
        convert_transaction_to_rub(transaction)

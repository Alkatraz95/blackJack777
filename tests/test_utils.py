import pytest
from unittest.mock import patch, MagicMock
from src.utils import convert_currency


@patch('src.utils.requests.get')
def test_convert_currency_success(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"rates": {"USD": 1.2}}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = convert_currency(100, "EUR", "USD")

    assert isinstance(result, float)
    assert result == pytest.approx(120.0)
    mock_get.assert_called_once()


@patch('src.utils.requests.get')
def test_convert_currency_missing_currency(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"rates": {}}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    with pytest.raises(ValueError):
        convert_currency(100, "EUR", "XYZ")


@patch('src.utils.requests.get')
def test_convert_currency_network_error(mock_get):
    mock_get.side_effect = Exception("Network error")

    with pytest.raises(Exception):
        convert_currency(100, "EUR", "USD")

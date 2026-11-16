"""Утилиты для работы с файлом транзакций и конвертацией валют."""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Tuple

import requests
from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parent.parent / ".env")

PATH_TO_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "operations.json")
BASE_URL = "https://api.apilayer.com/exchangerates_data/latest"
SUPPORTED_CURRENCIES = {"RUB", "USD", "EUR"}


def read_json_file(path_to_file: str = PATH_TO_FILE) -> List[Dict[str, Any]]:
    """Читает JSON-файл и возвращает список транзакций.

    Args:
        path_to_file: путь к JSON-файлу.

    Returns:
        Список словарей с транзакциями. Если файла нет или JSON некорректен — [].
    """
    try:
        with open(path_to_file, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    if not isinstance(data, list):
        return []
    return data


def _extract_amount_and_code(transaction: Dict[str, Any]) -> Tuple[Any, Any]:
    """Достаёт сумму и код валюты из вложенной структуры."""
    operation = transaction.get("operationAmount", {})
    amount = operation.get("amount")
    code = operation.get("currency", {}).get("code")
    return amount, code


def convert_transaction_to_rub(transaction: Dict[str, Any]) -> float:
    """Конвертирует сумму транзакции в рубли.

    Для RUB возвращает сумму без запроса к API.
    Для USD и EUR запрашивает курс через внешний API.

    Args:
        transaction: словарь с данными транзакции.

    Returns:
        Сумма в рублях, округлённая до 2 знаков.
    """
    amount, code = _extract_amount_and_code(transaction)

    if amount is None or code is None:
        raise ValueError("В транзакции отсутствует сумма или валюта")

    amount = float(amount)

    if code == "RUB":
        return round(amount, 2)

    if code not in SUPPORTED_CURRENCIES:
        raise ValueError(f"Неподдерживаемая валюта: {code}")

    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("Не задан API_KEY в переменных окружения")

    response = requests.get(
        BASE_URL,
        params={"base": code, "symbols": "RUB"},
        headers={"apikey": api_key},
        timeout=10,
    )
    response.raise_for_status()
    rate = response.json()["rates"]["RUB"]

    return round(amount * rate, 2)

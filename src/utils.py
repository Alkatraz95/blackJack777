import json
import os
from typing import Any, Dict, List

import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("API_KEY")


def read_json_file(path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON-файл и возвращает список словарей с транзакциями.

    Если файл не найден, содержит не список или повреждён — возвращается пустой список.

    Args:
        path: путь к JSON-файлу с данными о финансовых операциях.

    Returns:
        list: список словарей с транзакциями или пустой список при ошибках.
    """
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    if not isinstance(data, list):
        return []

    return data


def convert_transaction_to_rub(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли.

    Для USD и EUR запрашивает курс через внешний API. Для RUB возвращает сумму как есть.
    При неподдерживаемой валюте выбрасывает ValueError.

    Args:
        transaction: словарь с транзакцией, должен содержать ключи:
            - "amount": сумма (число или строка, приводимая к float)
            - "currency": код валюты (USD, EUR, RUB)

    Returns:
        float: сумма транзакции в рублях, округлённая до 2 знаков.

    Raises:
        ValueError: если валюта не поддерживается.
    """
    currency_code = transaction.get("currency", "RUB")
    try:
        amount = float(transaction["amount"])
    except (TypeError, ValueError):
        amount = 0.0

    if currency_code == "RUB":
        return round(amount, 2)

    if currency_code not in ("USD", "EUR"):
        raise ValueError(f"Валюта {currency_code} не поддерживается")

    url = "https://api.apilayer.com/exchangerates_data/convert"
    headers = {"apikey": API_KEY}
    params = {"from": currency_code, "to": "RUB", "amount": amount}

    response = requests.get(url, headers=headers, params=params, timeout=10)
    response.raise_for_status()

    result = response.json().get("result")
    if result is None:
        raise ValueError("Не удалось получить результат конвертации из ответа API")

    return round(float(result), 2)

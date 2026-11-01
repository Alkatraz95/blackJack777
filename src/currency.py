import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.apilayer.com/exchangerate_host/convert"
RUB_CURRENCIES = {"RUB", "RUR", ""}


def get_transaction_amount_in_rub(transaction: Dict[str, Any]) -> float:
    """Возвращает сумму транзакции в рублях.

    Если транзакция в USD или EUR — обращается к внешнему API за курсом.
    Если валюта RUB (или не указана) — возвращает amount без конвертации.
    """
    amount = float(transaction.get("amount", 0) or 0)
    currency = str(transaction.get("currency", "RUB")).upper().strip()

    if currency in RUB_CURRENCIES:
        return amount

    api_key = os.getenv("API_KEY", "")
    try:
        response = requests.get(
            API_URL,
            params={"from": currency, "to": "RUB", "amount": amount},
            headers={"apikey": api_key},
            timeout=5,
        )
        return float(response.json()["result"])
    except (requests.RequestException, KeyError, ValueError, TypeError):
        return amount

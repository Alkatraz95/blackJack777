import requests

def convert_currency(amount, from_currency, to_currency):
    """
    Конвертирует сумму из одной валюты в другую через API.
    Возвращает результат как float.

    Raises:
        ValueError: если курс для целевой валюты не найден.
        requests.RequestException: при ошибках сети/API.
    """
    url = "https://api.exchangerate-api.com/v4/latest"
    base = from_currency

    response = requests.get(f"{url}/{base}", timeout=5)
    response.raise_for_status()
    data = response.json()

    rates = data.get("rates", {})
    if to_currency not in rates:
        raise ValueError(f"Курс для валюты {to_currency} не найден")

    rate = rates[to_currency]
    converted = amount * rate

    return float(converted)

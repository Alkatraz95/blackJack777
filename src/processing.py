from datetime import datetime


def filter_by_state(dictionary_list: list[dict], state: str = "EXECUTED") -> list:
    """Функция принимает список словарей и возвращает новый список,
    содержащий только те словари, у которых ключ state соответствует указанному значению.
    """

    # Создаем пустой список для хранения отфильтрованных словарей
    filtered_list = []

    # Проходим по каждому элементу в исходном списке
    for item in dictionary_list:
        # Проверяем, есть ли ключ 'state' и соответствует ли значение ключа указанному состоянию
        if "state" in item and item["state"] == state:
            # Если да, добавляем элемент в отфильтрованный список
            filtered_list.append(item)

    # Возвращаем отфильтрованный список
    return filtered_list


if __name__ == "__main__":
    transactions = [
        {
            "id": 596171168,
            "state": "EXECUTED",
            "date": "2018-07-11T02:26:18.671407",
            "operationAmount": {
                "amount": "79931.03",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Открытие вклада",
            "to": "Счет 72082042523231456215",
        },
        {
            "id": 716496732,
            "state": "EXECUTED",
            "date": "2018-04-04T17:33:34.701093",
            "operationAmount": {
                "amount": "40701.91",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод организации",
            "from": "Visa Gold 5999414228426353",
            "to": "Счет 72731966109147704472",
        },
        {
            "id": 863064926,
            "state": "EXECUTED",
            "date": "2019-12-08T22:46:21.935582",
            "operationAmount": {
                "amount": "41096.24",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Открытие вклада",
            "to": "Счет 90424923579946435907",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
        {
            "id": 615064591,
            "state": "CANCELED",
            "date": "2018-10-14T08:21:33.419441",
            "operationAmount": {
                "amount": "77751.04",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод с карты на счет",
            "from": "Maestro 3928549031574026",
            "to": "Счет 84163357546688983493",
        },
    ]

executed_transactions = filter_by_state(transactions, state="EXECUTED")
print(executed_transactions)  # Выводит список транзакций со статусом EXECUTED


def sort_by_date(dictionary_list: list[dict], parameter: bool = True) -> list[dict]:
    """Функция, которая принимает список словарей и необязательный параметр,
    задающий порядок сортировки (по умолчанию — убывание). Функция должна возвращать новый список,
    отсортированный по дате (date)."""

    sort_list = sorted(dictionary_list, key=lambda x: x["date"], reverse=parameter)

    # Проверка корректности формата даты
    for item in dictionary_list:
        try:
            # Проверяем наличие 'Z' в конце строки даты
            if item["date"].endswith("Z"):
                # Формат без микросекунд
                datetime.strptime(item["date"], "%Y-%m-%dT%H:%M:%SZ")
            else:
                # Формат с микросекундами
                datetime.strptime(item["date"], "%Y-%m-%dT%H:%M:%S.%f")
        except ValueError:
            raise ValueError(f"Некорректный формат даты: {item['date']}")

    return sort_list


if __name__ == "__main__":
    transactions_list = [
        {
            "id": 596171168,
            "state": "EXECUTED",
            "date": "2018-07-11T02:26:18.671407",
            "operationAmount": {
                "amount": "79931.03",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Открытие вклада",
            "to": "Счет 72082042523231456215",
        },
        {
            "id": 716496732,
            "state": "EXECUTED",
            "date": "2018-04-04T17:33:34.701093",
            "operationAmount": {
                "amount": "40701.91",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод организации",
            "from": "Visa Gold 5999414228426353",
            "to": "Счет 72731966109147704472",
        },
        {
            "id": 863064926,
            "state": "EXECUTED",
            "date": "2019-12-08T22:46:21.935582",
            "operationAmount": {
                "amount": "41096.24",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Открытие вклада",
            "to": "Счет 90424923579946435907",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
        {
            "id": 615064591,
            "state": "CANCELED",
            "date": "2018-10-14T08:21:33.419441",
            "operationAmount": {
                "amount": "77751.04",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод с карты на счет",
            "from": "Maestro 3928549031574026",
            "to": "Счет 84163357546688983493",
        },
    ]

    # Сортировка по возрастанию
    dictionary_list = sort_by_date(transactions_list, parameter=False)
    print(dictionary_list)

    # Сортировка по вщзрастанию
    dictionary_list = sort_by_date(transactions_list, parameter=True)
    print(dictionary_list)


# python src/processing.py
# black src/processing.py
# flake8 src/processing.py
# mypy src/processing.py
# isort src/processing.py

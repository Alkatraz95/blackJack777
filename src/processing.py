from datetime import datetime
from typing import Any, Dict, List


def filter_by_state(dictionary_list: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    return [item for item in dictionary_list if isinstance(item, dict) and item.get("state") == state]


def sort_by_date(
    dictionary_list: List[Dict[str, Any]],
    reverse: bool = True,
) -> List[Dict[str, Any]]:

    def parse_date(date_str: str) -> datetime:
        if date_str.endswith("Z"):
            date_str = date_str[:-1] + "+00:00"
        return datetime.fromisoformat(date_str)

    for item in dictionary_list:
        if not isinstance(item, dict):
            raise TypeError(f"Ожидался dict, но получено: {type(item)}")
        if "date" not in item:
            raise ValueError("Отсутствует поле 'date' в транзакции")
        try:
            parse_date(item["date"])
        except ValueError as e:
            raise ValueError(f"Некорректный формат даты: {item['date']}") from e

    return sorted(
        dictionary_list,
        key=lambda x: parse_date(x["date"]),
        reverse=reverse,
    )


if __name__ == "__main__":  # pragma: no cover
    transactions = [
        {
            "id": 596171168,
            "state": "EXECUTED",
            "date": "2018-07-11T02:26:18.671407",
            "operationAmount": {"amount": "79931.03", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Открытие вклада",
            "to": "Счет 72082042523231456215",
        },
        {
            "id": 716496732,
            "state": "EXECUTED",
            "date": "2018-04-04T17:33:34.701093",
            "operationAmount": {"amount": "40701.91", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Visa Gold 5999414228426353",
            "to": "Счет 72731966109147704472",
        },
        {
            "id": 863064926,
            "state": "EXECUTED",
            "date": "2019-12-08T22:46:21.935582",
            "operationAmount": {"amount": "41096.24", "currency": {"name": "USD", "code": "USD"}},
            "description": "Открытие вклада",
            "to": "Счет 90424923579946435907",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
        {
            "id": 615064591,
            "state": "CANCELED",
            "date": "2018-10-14T08:21:33.419441",
            "operationAmount": {"amount": "77751.04", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод с карты на счет",
            "from": "Maestro 3928549031574026",
            "to": "Счет 84163357546688983493",
        },
    ]

    executed = filter_by_state(transactions, state="EXECUTED")
    print("EXECUTED:", len(executed))

    sorted_asc = sort_by_date(transactions, reverse=False)
    sorted_desc = sort_by_date(transactions, reverse=True)

    print("Первые 2 по возрастанию:", [t["id"] for t in sorted_asc[:2]])
    print("Первые 2 по убыванию:", [t["id"] for t in sorted_desc[:2]])

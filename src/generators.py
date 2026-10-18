from email import iterators


def filter_by_currency(transactions, code="USD"):
    """Функция, которая принимает на вход список словарей, представляющих транзакции.
    Функция должна возвращать итератор, который поочередно выдает транзакции,
     где валюта операции соответствует заданной (например, USD)."""

    for transaction in transactions:
        # Проверяем наличие ключа "operationAmount" и его вложенных ключей
        if (
            "operationAmount" in transaction
            and "currency" in transaction["operationAmount"]
            and "code" in transaction["operationAmount"]["currency"]
        ):
            if transaction["operationAmount"]["currency"]["code"] == code:
                yield transaction  # Генерируем транзакцию


if __name__ == "__main__":
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

    # Преобразуем итератор в список
    usd_transactions = list(filter_by_currency(transactions, code="USD"))
    print(usd_transactions)  # Выводит список словарей с транзакциями в USD


def transaction_descriptions(transactions):
    """Генератор transaction_descriptions,
    который принимает список словарей с транзакциями и возвращает описание каждой операции по очереди."""

    for transact in transactions:
        yield transact["description"]


# descriptions = transaction_descriptions(transactions)
# for _ in range(5):
#     print(next(descriptions))


def card_number_generator(start, end):
    """Функция (генератор), которая выдает номера банковских карт в формате XXXX XXXX XXXX XXXX,
     где X — цифра номера карты. Генератор может сгенерировать номера карт в заданном диапазоне от
     0000 0000 0000 0001 до 9999 9999 9999 9999.
    Генератор должен принимать начальное и конечное значения для генерации диапазона номеров."""

    for number in range(start, end + 1):
        yield f"{number:016d}"[:4] + " " + f"{number:016d}"[4:8] + " " + f"{number:016d}"[
            8:12
        ] + " " + f"{number:016d}"[12:]


# start_number = 1
# end_number = 10
#
# for card_number in card_number_generator(start_number, end_number):
#     print(card_number)


# python src/generators.py
# black src/generators.py
# flake8 src/generators.py
# mypy src/generators.py
# isort src/generators.py

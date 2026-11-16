"""Точка входа: консольный интерфейс проекта."""

from typing import Any

from src.readers import (read_transactions_from_csv,
                         read_transactions_from_excel)
from src.search import process_bank_search
from src.utils import read_json_file


VALID_STATUSES = {"EXECUTED", "CANCELED", "PENDING"}


def filter_by_status(transactions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Фильтрует транзакции по статусу (без учёта регистра)."""
    while True:
        status = input(
            "Введите статус, по которому необходимо выполнить фильтрацию. "
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"
        ).strip().upper()
        if status in VALID_STATUSES:
            print(f'Операции отфильтрованы по статусу "{status}"')
            return [t for t in transactions if str(t.get("state", "")).upper() == status]
        print(f'Статус операции "{status}" недоступен.')


def sort_transactions(transactions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Сортировка по дате (по запросу пользователя)."""
    choice = input("Отсортировать операции по дате? Да/Нет\n").strip().lower()
    if choice not in ("да", "yes", "y"):
        return transactions
    choice = input("По возрастанию или по убыванию?\n").strip().lower()
    reverse = "убывание" in choice
    return sorted(transactions, key=lambda x: str(x.get("date", "")), reverse=reverse)


def filter_rub(transactions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Оставляет только рублёвые транзакции (по запросу пользователя)."""
    choice = input("Выводить только рублевые транзакции? Да/Нет\n").strip().lower()
    if choice in ("да", "yes", "y"):
        return [
            t
            for t in transactions
            if str(t.get("currency_name", "")).upper() == "RUB"
        ]
    return transactions


def search_interface(transactions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Поиск по строке в description с помощью re."""
    choice = input(
        "Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n"
    ).strip().lower()
    if choice not in ("да", "yes", "y"):
        return transactions
    text = input("Строка для поиска: ").strip()
    return process_bank_search(transactions, text)


def print_result(transactions: list[dict[str, Any]]) -> None:
    """Вывод итогового списка."""
    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return
    print("Распечатываю итоговый список транзакций...\n")
    print(f"Всего банковских операций в выборке: {len(transactions)}")
    for t in transactions:
        date = str(t.get("date", ""))[:10].replace("-", ".")
        desc = t.get("description", "")
        amount = t.get("amount", "")
        currency = t.get("currency_name", "")
        print(f"\n{date} {desc}\nСумма: {amount} {currency}")


def main() -> None:
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    transactions: list[dict[str, Any]] = []

    while True:
        choice = input("Выбор: ").strip()
        if choice == "1":
            print("Для обработки выбран JSON-файл.")
            path = input("Путь к JSON-файлу: ").strip()
            transactions = read_json_file(path)
            break
        elif choice == "2":
            print("Для обработки выбран CSV-файл.")
            path = input("Путь к CSV-файлу: ").strip()
            transactions = read_transactions_from_csv(path)
            break
        elif choice == "3":
            print("Для обработки выбран XLSX-файл.")
            path = input("Путь к XLSX-файлу: ").strip()
            transactions = read_transactions_from_excel(path)
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

    transactions = filter_by_status(transactions)
    transactions = sort_transactions(transactions)
    transactions = filter_rub(transactions)
    transactions = search_interface(transactions)
    print_result(transactions)


if __name__ == "__main__":
    main()

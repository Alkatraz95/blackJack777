"""Точка входа: консольный интерфейс проекта."""

from typing import Any

from src.readers import (read_transactions_from_csv,
                         read_transactions_from_excel)
from src.search import process_bank_search
from src.utils import read_json_file
from src.widget import get_date, mask_account_card


VALID_STATUSES = {"EXECUTED", "CANCELED", "PENDING"}


def format_route(transaction: dict[str, Any]) -> str:
    """Формирует строку перевода с маскированными реквизитами."""
    parts = []
    for key in ("from", "to"):
        value = str(transaction.get(key, "") or "")
        if not value:
            continue
        try:
            masked = mask_account_card(value)
            if value.split()[0] == "Счет" and not masked.startswith("Счет"):
                masked = f"Счет {masked}"
            parts.append(masked)
        except ValueError:
            parts.append(value)
    return " -> ".join(parts)


def format_currency(name: Any) -> str:
    """Возвращает название валюты в формате задания."""
    value = str(name)
    return "руб." if value.upper() == "RUB" else value


def filter_by_status(transactions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Фильтрует транзакции по статусу (без учёта регистра)."""
    while True:
        status = input(
            "Введите статус, по которому необходимо выполнить фильтрацию. "
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"
        ).strip().upper()
        if status in VALID_STATUSES:
            print(f'Операции отфильтрованы по статусу "{status}"')
            return [t for t in transactions
                    if str(t.get("state", "")).upper() == status]
        print(f'Статус операции "{status}" недоступен.')


def sort_transactions(transactions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Сортировка по дате (по запросу пользователя)."""
    choice = input("Отсортировать операции по дате? Да/Нет\n").strip().lower()
    if choice not in ("да", "yes", "y"):
        return transactions
    choice = input("По возрастанию или по убыванию?\n").strip().lower()
    reverse = "убывани" in choice
    return sorted(transactions,
                  key=lambda x: str(x.get("date", "")),
                  reverse=reverse)


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
    print("Распечатываю итоговый список транзакций...\n")
    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return
    print(f"Всего банковских операций в выборке: {len(transactions)}")
    for t in transactions:
        raw_date = str(t.get("date", ""))
        try:
            date = get_date(raw_date)
        except (ValueError, TypeError):
            date = raw_date
        print(f"\n{date} {t.get('description', '')}")
        route = format_route(t)
        if route:
            print(route)
        amount = t.get("amount", "")
        currency = format_currency(t.get("currency_name", ""))
        print(f"Сумма: {amount} {currency}")


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

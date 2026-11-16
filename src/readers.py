"""Модуль для считывания финансовых операций из CSV- и Excel-файлов."""

import csv

import pandas as pd


def read_transactions_from_csv(path: str) -> list[dict]:
    """Считывает финансовые операции из CSV-файла.

    Args:
        path: путь к CSV-файлу с транзакциями.

    Returns:
        Список словарей с транзакциями. Ключи — названия столбцов,
        значения — данные из соответствующих ячеек. Пустые строки
        (без значений ни в одном столбце) отбрасываются.
    """
    with open(path, 'r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f, delimiter=';')
        return [row for row in reader if any(row.values())]


def read_transactions_from_excel(path: str) -> list[dict]:
    """Считывает финансовые операции из Excel-файла.

    Args:
        path: путь к XLSX-файлу с транзакциями.

    Returns:
        Список словарей с транзакциями. Каждая строка таблицы
        преобразуется в отдельный словарь.
    """
    df = pd.read_excel(path, engine='openpyxl')
    return df.to_dict(orient='records')

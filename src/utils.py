import json
from typing import Any, Dict, List


def read_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Читает JSON-файл со списком транзакций.

    Возвращает список словарей. При любой ошибке (файл не найден,
    битый JSON, пустой файл, объект вместо списка) возвращает [].
    """
    try:
        # utf-8-sig автоматически игнорирует BOM, если он есть в файле
        with open(file_path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []

    if not isinstance(data, list):
        return []

    return [item for item in data if isinstance(item, dict)]

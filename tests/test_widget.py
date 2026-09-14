import pytest
from src.widget import get_date


@pytest.mark.parametrize(
    "input_date, expected",
    [
        ("2023-12-31", "31.12.2023"),
        ("2020-02-29", "29.02.2020"),
        ("1999-01-01", "01.01.1999"),
        ("2000-12-31T23:59:59", "31.12.2000"),
        ("2023-06-15T00:00:00", "15.06.2023"),  # убрали Z
    ],
)
def test_standard_date_formats(input_date: str, expected: str) -> None:
    """Проверяем корректное преобразование стандартных форматов дат"""
    assert get_date(input_date) == expected


# Тест для граничных случаев — оставляем как есть
@pytest.mark.parametrize(
    "input_date, expected",
    [
        ("0001-01-01", "01.01.0001"),
        ("9999-12-31", "31.12.9999"),
        ("1970-01-01", "01.01.1970"),
    ],
)
def test_edge_cases(input_date: str, expected: str) -> None:
    """Проверяем обработку граничных случаев"""
    assert get_date(input_date) == expected
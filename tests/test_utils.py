import pytest
from src.utils import convert_currency


def test_convert_currency_success():
    # Базовые проверки
    assert convert_currency(90, "RUB", "USD") == 1.0
    assert convert_currency(180, "RUB", "USD") == 2.0

    # Проверка конвертации между другими валютами (через USD)
    # 90 RUB → 1 USD → 0.85 EUR
    result = convert_currency(90, "RUB", "EUR")
    expected = 90 / 90 * 0.85  # 0.85
    assert result == pytest.approx(expected, rel=1e-3)


def test_convert_currency_missing_currency():
    with pytest.raises(ValueError) as exc_info:
        convert_currency(100, "XYZ", "USD")
    assert "Неизвестный код валюты" in str(exc_info.value)

    with pytest.raises(ValueError) as exc_info:
        convert_currency(100, "RUB", "ABC")
    assert "Неизвестный код валюты" in str(exc_info.value)


def test_convert_currency_edge_cases():
    # Ноль — всегда 0.0
    assert convert_currency(0, "RUB", "USD") == 0.0

    # Очень маленькое число: из-за round(..., 2) результат будет 0.0
    # Это ожидаемое поведение функции
    assert convert_currency(0.01, "RUB", "USD") == pytest.approx(0.0, rel=1e-3)

    # Число, которое после конвертации и округления даст заметный результат
    # 1 RUB → 1/90 ≈ 0.0111 → round до 0.01
    assert convert_currency(1, "RUB", "USD") == pytest.approx(0.01, rel=1e-2)

    # Ещё одна проверка: 50 RUB → 50/90 ≈ 0.555 → round до 0.56
    assert convert_currency(50, "RUB", "USD") == pytest.approx(0.56, rel=1e-2)

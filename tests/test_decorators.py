import pytest

from src.decorators import log


# Пример функции для тестирования
@log()
def add(a, b):
    return a + b


@log()
def divide(a, b):
    return a / b


# Тест успешного выполнения функции add


def test_add_success(capsys):
    result = add(5, 7)
    captured = capsys.readouterr()
    assert result == 12
    assert "Начало выполнения функции: add" in captured.out
    assert "Функция: add, Результат: 12" in captured.out
    assert "Конец выполнения функции: add" in captured.out


# Тест успешного выполнения функции divide


def test_divide_success(capsys):
    result = divide(10, 2)
    captured = capsys.readouterr()
    assert result == 5.0
    assert "Начало выполнения функции: divide" in captured.out
    assert "Функция: divide, Результат: 5.0" in captured.out
    assert "Конец выполнения функции: divide" in captured.out


# Тест обработки исключения в функции divide


def test_divide_zero(capsys):
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
    captured = capsys.readouterr()
    assert "Начало выполнения функции: divide" in captured.out
    assert "Функция: divide, Ошибка: ZeroDivisionError, Параметры: (10, 0), {}" in captured.out
    assert "Конец выполнения функции: divide" in captured.out


# black tests/test_decorators.py

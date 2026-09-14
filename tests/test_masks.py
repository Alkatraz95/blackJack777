import pytest

from src.masks import get_mask_account
from src.masks import get_mask_card_number


# Позитивные тесты - проверка корректного маскирования
@pytest.mark.parametrize(
    "card_number, expected_mask",
    [
        ("7000792289606361", "7000 79** **** 6361"),  # Стандартный номер
        ("0000000000000000", "0000 00** **** 0000"),  # Номер из нулей
        ("1234567812345678", "1234 56** **** 5678"),  # Другой номер
    ],
)
def test_card_masking_correct(card_number: str, expected_mask: str) -> None:
    """Проверяем корректное маскирование валидных номеров карт"""
    assert get_mask_card_number(card_number) == expected_mask


# Негативные тесты - проверка обработки ошибок
@pytest.mark.parametrize(
    "invalid_input, expected_error",
    [
        (None, "Номер карты не может быть None"),  # явно проверяем None
        ("", "Номер карты должен состоять из 16 цифр"),
        ("1234", "Номер карты должен состоять из 16 цифр"),
        ("abcdefghijklmnop", "Номер карты должен состоять из 16 цифр"),
        ("123456781234567890", "Номер карты должен состоять из 16 цифр"),
    ],
)
def test_card_masking_errors(invalid_input: str, expected_error: str) -> None:
    """Проверяем обработку невалидных номеров карт"""
    with pytest.raises(ValueError) as exc_info:
        get_mask_card_number(invalid_input)
    assert str(exc_info.value) == expected_error


# Позитивные тесты - проверка корректного маскирования
@pytest.mark.parametrize(
    "account_number, expected_mask",
    [
        ("7000792289606361", "**6361"),  # 16 цифр
        ("00000000", "**0000"),  # 8 цифр
        ("123456", "**3456"),  # Минимальная длина (6 цифр)
        ("12345678901234567890", "**7890"),  # 20 цифр
    ],
)
def test_account_masking_correct(account_number: str, expected_mask: str) -> None:
    """Проверяем корректное маскирование валидных номеров счетов"""
    assert get_mask_account(account_number) == expected_mask


# Негативные тесты - проверка обработки ошибок
@pytest.mark.parametrize(
    "invalid_input, expected_error",
    [
        (None, "Номер счета не может быть None"),  # Специальная проверка для None
        ("", "Номер счета должен состоять из цифр"),  # Пустая строка
        ("1234", "Номер счета должен состоять из цифр"),  # Слишком короткий (4 цифры)
        ("abcd", "Номер счета должен состоять из цифр"),  # Буквы
        ("1234-5678", "Номер счета должен состоять из цифр"),  # С разделителями
        ("12 3456", "Номер счета должен состоять из цифр"),  # С пробелами
        ("12345", "Номер счета должен состоять из цифр"),  # 5 цифр (меньше минимальных 6)
        ("123.456", "Номер счета должен состоять из цифр"),  # С точкой
    ],
)
def test_account_masking_errors(invalid_input: str, expected_error: str) -> None:
    """Проверяем обработку невалидных номеров счетов"""
    with pytest.raises(ValueError) as exc_info:
        get_mask_account(invalid_input)
    assert str(exc_info.value) == expected_error


# Граничные случаи
def test_account_min_length() -> None:
    """Проверяем минимально допустимую длину номера счета (6 цифр)"""
    assert get_mask_account("123456") == "**3456"
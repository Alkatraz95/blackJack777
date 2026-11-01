import pytest

from src.masks import get_mask_account
from src.masks import get_mask_card_number


# Позитивные тесты — маскирование карт
@pytest.mark.parametrize(
    "card_number, expected_mask",
    [
        ("7000792289606361", "7000 79** **** 6361"),
        ("0000000000000000", "0000 00** **** 0000"),
        ("1234567812345678", "1234 56** **** 5678"),
    ],
)
def test_card_masking_correct(card_number: str, expected_mask: str) -> None:
    assert get_mask_card_number(card_number) == expected_mask


# Негативные тесты — ошибки карт
@pytest.mark.parametrize(
    "invalid_input, expected_error",
    [
        (None, "Номер карты не может быть None"),
        ("", "Номер карты должен состоять из 16 цифр"),
        ("1234", "Номер карты должен состоять из 16 цифр"),
        ("abcdefghijklmnop", "Номер карты должен состоять из 16 цифр"),
        ("123456781234567890", "Номер карты должен состоять из 16 цифр"),
    ],
)
def test_card_masking_errors(invalid_input, expected_error: str) -> None:
    with pytest.raises(ValueError) as exc_info:
        get_mask_card_number(invalid_input)
    assert str(exc_info.value) == expected_error


# Позитивные тесты — маскирование счетов
@pytest.mark.parametrize(
    "account_number, expected_mask",
    [
        ("7000792289606361", "**6361"),
        ("00000000", "**0000"),
        ("123456", "**3456"),
        ("12345678901234567890", "**7890"),
    ],
)
def test_account_masking_correct(account_number: str, expected_mask: str) -> None:
    assert get_mask_account(account_number) == expected_mask


# Негативные тесты — ошибки счетов
@pytest.mark.parametrize(
    "invalid_input, expected_error",
    [
        (None, "Номер счета не может быть None"),
        ("", "Номер счета должен состоять из цифр"),
        ("1234", "Номер счета должен состоять из цифр"),
        ("abcd", "Номер счета должен состоять из цифр"),
        ("1234-5678", "Номер счета должен состоять из цифр"),
        ("12 3456", "Номер счета должен состоять из цифр"),
        ("12345", "Номер счета должен состоять из цифр"),
        ("123.456", "Номер счета должен состоять из цифр"),
    ],
)
def test_account_masking_errors(invalid_input, expected_error: str) -> None:
    with pytest.raises(ValueError) as exc_info:
        get_mask_account(invalid_input)
    assert str(exc_info.value) == expected_error


# Граничный случай — минимальная длина счёта
def test_account_min_length() -> None:
    assert get_mask_account("123456") == "**3456"

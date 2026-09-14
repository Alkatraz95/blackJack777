import pytest
from src.widget import mask_account_card, get_date


@pytest.mark.parametrize(
    "pay_info, expected",
    [
        # Счёт: оставляем 4 последние цифры
        ("Счет 72082042523231456215", "**6215"),
        ("Счет 123456", "**3456"),

        # Карта: формат "XXXX XX** **** XXXX" (4+2+4+4), но последние 4 цифры видны
        ("Card 4100123456789010", "4100 12** **** 9010"),
        ("Visa 4100123456789010", "4100 12** **** 9010"),
        ("MasterCard 1111222233334444", "1111 22** **** 4444"),
    ],
)
def test_mask_account_card_valid(pay_info: str, expected: str) -> None:
    assert mask_account_card(pay_info) == expected


@pytest.mark.parametrize("pay_info", [None, "", "   ", "Счет", "4100123456789010"])
def test_mask_account_card_invalid_format(pay_info) -> None:
    with pytest.raises(ValueError):
        mask_account_card(pay_info)


def test_mask_account_card_non_string() -> None:
    with pytest.raises(ValueError):
        mask_account_card(12345)


def test_mask_account_card_internal_error_account() -> None:
    # Если номер слишком короткий, get_mask_account выбросит ошибку
    with pytest.raises(ValueError, match="Ошибка обработки номера"):
        mask_account_card("Счет 123")


def test_mask_account_card_internal_error_card() -> None:
    with pytest.raises(ValueError, match="Ошибка обработки номера"):
        mask_account_card("Card 12345")


@pytest.mark.parametrize(
    "date_string, expected",
    [
        ("2019-07-03T18:35:29.512364", "03.07.2019"),
        ("2018-06-30T02:08:58.425572", "30.06.2018"),
        ("2023-01-01T00:00:00", "01.01.2023"),
    ],
)
def test_get_date_valid(date_string: str, expected: str) -> None:
    assert get_date(date_string) == expected


def test_get_date_invalid_iso() -> None:
    with pytest.raises(ValueError):
        get_date("не-дата")


def test_get_date_empty_string() -> None:
    with pytest.raises(ValueError):
        get_date("")

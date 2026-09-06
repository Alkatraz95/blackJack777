from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(card_info: str) -> str:
    """Принимает строку с типом и номером карты/счёта, возвращает замаскированную строку."""

    digits = ""
    letters = ""

    for ch in card_info:
        if ch.isdigit():
            digits += ch
        elif ch.isalpha():
            letters += ch

    if len(digits) == 16:
        return f"{letters} {get_mask_card_number(digits)}"
    elif len(digits) == 20:
        return f"{letters} {get_mask_account(digits)}"
    else:
        raise ValueError(
            f"Не удалось определить тип: найдено {len(digits)} цифр. "
            "Ожидается 16 (карта) или 20 (счёт)."
        )


def get_date(date_str: str) -> str:
    """Принимает дату в формате ISO, возвращает строку 'ДД.ММ.ГГГГ'."""

    date_format = '"ДД.ММ.ГГГГ"'
    day = date_str[8:10]
    month = date_str[5:7]
    year = date_str[:4]

    return f'{date_format}  ( "{day}.{month}.{year}" ).'


if __name__ == "__main__":
    print(mask_account_card("Счет 64686473678894779589"))
    print(mask_account_card("Maestro 1596837868705199"))
    print(get_date("2024-03-11T02:26:18.671407"))

def get_mask_card_number(card_number: str) -> str:
    """
    Возвращает замаскированный номер карты в формате XXXX XX** **** XXXX.
    Оставляет первые 6 и последние 4 цифры, остальное заменяет на *.
    Входная строка может содержать пробелы/дефисы — они удаляются.
    """
    # Оставляем только цифры
    digits = "".join(ch for ch in card_number if ch.isdigit())

    if len(digits) < 10:
        raise ValueError("Номер карты слишком короткий")

    first_part = digits[:6]
    last_part = digits[-4:]
    masked_middle = "*" * (len(digits) - 10)

    full_masked = first_part + masked_middle + last_part

    # Форматируем в группы по 4 для читаемости: XXXX XX** **** XXXX
    # Сначала разобьём на куски по 4 символа
    chunks = [full_masked[i : i + 4] for i in range(0, len(full_masked), 4)]
    return " ".join(chunks)


def get_mask_account(account_number: str) -> str:
    """
    Возвращает замаскированный номер счёта в формате **XXXX.
    Показывает только последние 4 цифры.
    Входная строка может содержать лишние символы — они удаляются.
    """
    digits = "".join(ch for ch in account_number if ch.isdigit())

    if len(digits) < 4:
        raise ValueError("Номер счёта слишком короткий")

    last_four = digits[-4:]
    return f"**{last_four}"


if __name__ == "__main__":
    print(get_mask_card_number("1596837868705199"))
    print(get_mask_account("64686473678894779589"))

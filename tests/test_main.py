"""Тесты консольного интерфейса main."""

from unittest.mock import patch

from src import main as main_module


@patch("builtins.input")
def test_filter_by_status_valid(mock_input):
    """Корректный статус фильтрует транзакции."""
    mock_input.return_value = "EXECUTED"
    data = [{"state": "EXECUTED", "amount": 1}, {"state": "CANCELED", "amount": 2}]
    result = main_module.filter_by_status(data)
    assert len(result) == 1
    assert result[0]["state"] == "EXECUTED"


@patch("builtins.input")
def test_filter_by_status_retry(mock_input):
    """Неверный статус — повторный ввод."""
    mock_input.side_effect = ["test", "CANCELED"]
    data = [{"state": "CANCELED", "amount": 2}]
    result = main_module.filter_by_status(data)
    assert len(result) == 1


@patch("builtins.input")
def test_sort_transactions_desc(mock_input):
    """Сортировка по убыванию даты."""
    mock_input.side_effect = ["да", "по убыванию"]
    data = [
        {"date": "2019-08-26T10:50:58"},
        {"date": "2020-01-15T12:00:00"},
    ]
    result = main_module.sort_transactions(data)
    assert result[0]["date"] > result[1]["date"]


@patch("builtins.input")
def test_sort_transactions_asc(mock_input):
    """Сортировка по возрастанию даты."""
    mock_input.side_effect = ["да", "по возрастанию"]
    data = [
        {"date": "2020-01-15T12:00:00"},
        {"date": "2019-08-26T10:50:58"},
    ]
    result = main_module.sort_transactions(data)
    assert result[0]["date"] < result[1]["date"]


@patch("builtins.input")
def test_sort_transactions_skip(mock_input):
    """Отказ от сортировки возвращает список без изменений."""
    mock_input.return_value = "нет"
    data = [{"date": "2019-08-26T10:50:58"}]
    assert main_module.sort_transactions(data) == data


@patch("builtins.input")
def test_filter_rub_yes(mock_input):
    """Фильтр только рублёвых транзакций."""
    mock_input.return_value = "да"
    data = [
        {"currency_name": "RUB"},
        {"currency_name": "USD"},
    ]
    result = main_module.filter_rub(data)
    assert len(result) == 1
    assert result[0]["currency_name"] == "RUB"


@patch("builtins.input")
def test_filter_rub_no(mock_input):
    """Отказ от фильтра возвращает список без изменений."""
    mock_input.return_value = "нет"
    data = [{"currency_name": "USD"}]
    assert main_module.filter_rub(data) == data


@patch("builtins.input")
def test_search_interface(mock_input):
    """Поиск по слову в описании вызывает process_bank_search."""
    mock_input.side_effect = ["да", "Перевод"]
    data = [{"description": "Перевод организации"}, {"description": "Вклад"}]
    result = main_module.search_interface(data)
    assert len(result) == 1
    assert result[0]["description"] == "Перевод организации"


@patch("builtins.input")
def test_search_interface_skip(mock_input):
    """Отказ от поиска возвращает список без изменений."""
    mock_input.return_value = "нет"
    data = [{"description": "Перевод организации"}]
    assert main_module.search_interface(data) == data


def test_print_result_empty(capsys):
    """Пустая выборка — сообщение об отсутствии операций."""
    main_module.print_result([])
    out = capsys.readouterr().out
    assert "Не найдено ни одной транзакции" in out


def test_print_result_filled(capsys):
    """Вывод непустой выборки: дата, описание, сумма."""
    main_module.print_result([
        {
            "date": "2019-08-26T10:50:58.216",
            "description": "Перевод организации",
            "from": "Счет 7365413842738789",
            "to": "Счет 7365413842738378",
            "amount": 1000,
            "currency_name": "RUB",
        }
    ])
    out = capsys.readouterr().out
    assert "26.08.2019" in out
    assert "Счет **8789" in out
    assert "Сумма: 1000 руб." in out


@patch("src.main.read_json_file")
@patch("builtins.input")
def test_main_json_flow(mock_input, mock_read, capsys):
    """Полный цикл main: JSON-файл, фильтр по статусу, вывод итога."""
    mock_read.return_value = [{
        "date": "2019-08-26T10:50:58.216",
        "description": "Перевод организации",
        "state": "EXECUTED",
        "amount": 1000,
        "currency_name": "RUB",
    }]
    mock_input.side_effect = [
        "1",        # пункт меню
        "ops.json", # путь
        "EXECUTED", # статус
        "нет",      # сортировка
        "нет",      # только RUB
        "нет",      # поиск
    ]
    main_module.main()
    captured = capsys.readouterr().out
    assert "Всего банковских операций в выборке: 1" in captured
    assert "26.08.2019" in captured
    assert "руб." in captured


@patch("src.main.read_json_file")
@patch("builtins.input")
def test_main_invalid_menu(mock_input, mock_read, capsys):
    """Неверный пункт меню — повторный запрос выбора."""
    mock_read.return_value = []
    mock_input.side_effect = [
        "9",        # неверный пункт
        "1",        # повторный выбор
        "ops.json", # путь
        "EXECUTED", # статус
        "нет",      # сортировка
        "нет",      # только RUB
        "нет",      # поиск
    ]
    main_module.main()
    captured = capsys.readouterr().out
    assert "Неверный выбор" in captured


@patch("src.main.read_transactions_from_csv")
@patch("builtins.input")
def test_main_does_not_crash(mock_input, mock_read):
    """Смоук-тест: main на CSV-потоке не падает."""
    mock_read.return_value = [{"id": "1", "description": "Покупка", "state": "EXECUTED"}]
    mock_input.side_effect = [
        "2",        # пункт 2 (CSV)
        "data.csv", # путь
        "EXECUTED", # статус
        "нет",      # сортировка
        "да",       # только RUB
        "нет",      # поиск
    ]
    main_module.main()

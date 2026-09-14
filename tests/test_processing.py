import pytest
from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_data():
    return [
        {
            "id": 41428829,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364",
        },
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
        },
        {
            "id": 615064591,
            "state": "CANCELED",
            "date": "2018-10-14T08:21:33.419441",
        },
    ]


# --- filter_by_state ---

def test_filter_by_state_executed(sample_data):
    result = filter_by_state(sample_data, "EXECUTED")
    assert len(result) == 2
    assert all(item["state"] == "EXECUTED" for item in result)


def test_filter_by_state_canceled(sample_data):
    result = filter_by_state(sample_data, "CANCELED")
    assert len(result) == 2
    assert all(item["state"] == "CANCELED" for item in result)


def test_filter_by_state_empty_list():
    assert filter_by_state([], "EXECUTED") == []


def test_filter_by_state_non_dict_items():
    # Проверяем, что не-dict элементы просто пропускаются (list comp)
    mixed = [
        {"state": "EXECUTED"},
        "not a dict",
        None,
        {"state": "CANCELED"},
    ]
    result = filter_by_state(mixed, "EXECUTED")
    assert len(result) == 1
    assert result[0]["state"] == "EXECUTED"


# --- sort_by_date: нормальные случаи ---

def test_sort_by_date_normal_desc(sample_data):
    # По умолчанию reverse=True — самые свежие первыми
    result = sort_by_date(sample_data)
    dates = [item["date"] for item in result]
    assert dates == sorted(dates, reverse=True)


def test_sort_by_date_asc(sample_data):
    result = sort_by_date(sample_data, reverse=False)
    dates = [item["date"] for item in result]
    assert dates == sorted(dates)


def test_sort_by_date_empty_list():
    assert sort_by_date([]) == []


def test_sort_by_date_single_item():
    data = [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2023-01-01T00:00:00.000000",
        }
    ]
    result = sort_by_date(data)
    assert result == data


# --- sort_by_date: валидация и ошибки ---

def test_sort_by_date_missing_date_key():
    bad_data = [
        {"id": 1},  # нет поля date
        {"id": 2, "date": "2023-01-01T00:00:00.000000"},
    ]
    with pytest.raises(ValueError, match="Отсутствует поле 'date'"):
        sort_by_date(bad_data)


def test_sort_by_date_non_dict_item():
    bad_data = [
        {"date": "2023-01-01T00:00:00.000000"},
        "not a dict",
    ]
    with pytest.raises(TypeError, match="Ожидался dict"):
        sort_by_date(bad_data)


def test_sort_by_date_invalid_iso_format():
    bad_data = [
        {"date": "not-a-date"},
    ]
    with pytest.raises(ValueError, match="Некорректный формат даты"):
        sort_by_date(bad_data)


def test_sort_by_date_with_z_suffix():
    # Проверка обработки суффикса Z (код внутри parse_date)
    data_with_z = [
        {"date": "2023-01-01T12:00:00Z"},
        {"date": "2022-01-01T12:00:00Z"},
    ]
    result = sort_by_date(data_with_z, reverse=True)
    # Должны отсортироваться корректно, без ошибок
    assert len(result) == 2
    # Самая свежая дата должна быть первой
    assert result[0]["date"] == "2023-01-01T12:00:00Z"


def test_sort_by_date_mixed_valid_invalid():
    # Если хотя бы один элемент невалиден — функция должна упасть
    bad_data = [
        {"date": "2023-01-01T00:00:00.000000"},
        {"date": "invalid"},
    ]
    with pytest.raises(ValueError, match="Некорректный формат даты"):
        sort_by_date(bad_data)

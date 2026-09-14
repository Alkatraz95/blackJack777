import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def valid_filter_by_state():
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture
def expected_filter_by_state():
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]


def test_valid_filter_by_state(
    valid_filter_by_state, expected_filter_by_state, state="EXECUTED"
):

    filtered_result = filter_by_state(valid_filter_by_state, state)
    assert filtered_result == expected_filter_by_state


@pytest.fixture
def valid_filter_not_state():
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture
def expected_filter_not_state():
    return [
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


def test_valid_filter_not_state(
    valid_filter_not_state, expected_filter_not_state, state="CANCELED"
):

    filtered_result = filter_by_state(valid_filter_not_state, state)
    assert filtered_result == expected_filter_not_state


@pytest.mark.parametrize(
    "state, expected",
    [
        (
            "EXECUTED",
            {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        ),
        (
            "EXECUTED",
            {
                "id": 939719570,
                "state": "EXECUTED",
                "date": "2018-06-30T02:08:58.425572",
            },
        ),
        (
            "CANCELED",
            {
                "id": 594226727,
                "state": "CANCELED",
                "date": "2018-09-12T21:27:25.241689",
            },
        ),
        (
            "CANCELED",
            {
                "id": 615064591,
                "state": "CANCELED",
                "date": "2018-10-14T08:21:33.419441",
            },
        ),
    ],
)
def test_filter_by_state(state, expected):
    assert filter_by_state([expected], state) == [expected]


@pytest.fixture
def valid_sort_by_date():
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture
def expected_sort_by_date():
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]


@pytest.fixture
def expected_ascending_sort_by_date():
    return [
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    ]


def test_valid_sort_by_date(valid_sort_by_date, expected_sort_by_date):
    filtered_result = sort_by_date(valid_sort_by_date)
    assert filtered_result == expected_sort_by_date


def sort_by_date_ascending(data):
    return sorted(data, key=lambda x: x["date"])


def test_ascending_sort_by_date(valid_sort_by_date, expected_ascending_sort_by_date):
    filtered_result = sort_by_date_ascending(valid_sort_by_date)
    assert filtered_result == expected_ascending_sort_by_date


@pytest.mark.parametrize(
    "dictionary_list",
    [
        [{"date": "01-01-2023"}],  # Некорректный формат
        [{"date": "2023-01-01"}, {"date": "2022-15-05"}],  # Некорректный день
    ],
)
def test_sort_by_date_incorrect(dictionary_list):
    with pytest.raises(ValueError, match=r"Некорректный формат даты"):
        sort_by_date(dictionary_list)


# black tests/test_processing.py
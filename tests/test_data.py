from pathlib import Path

import pytest

from data import TransportData

DATA_PATH = Path(__file__).parent.parent / "data" / "processed" / "panel.csv"


@pytest.fixture
def data():
    """A TransportData object loaded with the real CSV. Shared by the tests"""
    return TransportData(DATA_PATH)


def test_year_range_returns_first_and_last_year(data):
    assert data.year_range() == (2015, 2024)


def test_filter_keeps_only_selected_countries_and_years(data):
    rows = data.filter(["PT", "NO"], 2020, 2022)

    assert set(rows["country"]) == {"PT", "NO"}
    assert rows["year"].min() >= 2020
    assert rows["year"].max() <= 2022


def test_countries_returns_25_pairs(data):
    assert len(data.countries()) == 25


def test_countries_returns_code_and_name(data):
    assert data.countries()[0] == ("AT", "Austria")


def test_every_row_has_country_name(data):
    assert data.df["country_name"].isna().sum() == 0


def test_one_year_returns_one_year(data):
    year = data.one_year(2024)

    assert set(year["year"]) == {2024}


def test_yearly_average_returns_one_row_per_year(data):
    averages = data.yearly_average("emission_pc")

    assert len(averages) == 10


def test_key_stats_return_none_for_empty_table(data):
    table = data.filter(["XX"], 2015, 2024)

    assert data.key_stats(table, "emission_pc") is None


def test_key_stats_returns_the_correct_values(data):
    table = data.filter(["PT", "DE", "NO", "ES"], 2018, 2024)

    values = data.key_stats(table, "emission_pc")

    assert values["highest"] == "Norway"
    assert values["lowest"] == "Portugal"
    assert values["change_pct"] == -10.4
    assert values["first_year"] == 2018
    assert values["latest_year"] == 2024


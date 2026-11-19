import pytest

from app import app


@pytest.fixture
def client():
    """A Flask test client: sends requests to the app without a browser or server"""
    return app.test_client()


def test_explore_ignores_unknown_indicator(client):
    response = client.get("/explore?indicator=hello")

    assert response.status_code == 200


def test_dashboard_loads(client):
    response = client.get("/")

    assert response.status_code == 200


def test_explore_loads_with_no_filters(client):
    response = client.get("/explore")

    assert response.status_code == 200


def test_bad_year_does_not_crash(client):
    response = client.get("/explore?start=abc")

    assert response.status_code == 200


def test_impossible_selection_shows_no_data_message(client):
    html = client.get("/explore?country=XX").get_data(as_text=True)

    assert "No data" in html


def test_selection_appears_on_page(client):
    html = client.get("/explore?country=PT").get_data(as_text=True)

    assert '"name":"Portugal"' in html
    assert '"name":"Spain"' not in html

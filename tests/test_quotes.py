from datetime import date

from app.internal import daily_quotes
from app.main import app

DATE = date(2021, 1, 1)
DATE2 = date(2021, 1, 2)
HOME_URL = app.url_path_for("home")
FAVORITE_QUOTES_URL = app.url_path_for("favorite_quotes")


def test_get_quote():
    quotes_fields = {
        "text": "some_quote",
        "author": "Freud",
    }
    result = daily_quotes.get_quote(quotes_fields)
    assert result.text == "some_quote"
    assert result.author == "Freud"


def test_get_quote_of_day_no_quotes(session):
    assert daily_quotes.get_quote_of_day(session, DATE) is None


def test_get_quote_of_day_get_first_quote(session, quote1, quote2):
    assert daily_quotes.get_quote_of_day(session, DATE).text == quote1.text


def test_get_quote_of_day_get_second_quote(session, quote1, quote2):
    assert daily_quotes.get_quote_of_day(session, DATE2).text == quote2.text


def test_save_quote(
    session,
    settings_test_client,
    quote1,
):
    data = {
        "user_id": 1,
        "quote": quote1.text,
        "author": quote1.author,
        "to_save": True,
    }
    response = settings_test_client.post(url=HOME_URL, data=data)
    assert response.ok


def test_delete_quote(session, settings_test_client, quote1):
    test_save_quote(session, settings_test_client, quote1)
    data = {
        "user_id": 1,
        "quote": quote1.text,
        "to_save": False,
    }
    response = settings_test_client.delete(url=HOME_URL, data=data)
    assert response.ok
    assert len(daily_quotes.get_quotes(session, 1)) == 0


def test_get_favorite_quotes(session, settings_test_client, quote1):
    test_save_quote(session, settings_test_client, quote1)
    response = settings_test_client.get(url=FAVORITE_QUOTES_URL)
    assert response.ok
    assert b"Favorite Quotes" in response.content

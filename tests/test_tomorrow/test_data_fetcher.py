import pytest
from unittest.mock import patch, MagicMock
from tomorrow.models import WeatherDataDaily, WeatherDataHourly, WeatherDataMinutely
from sqlalchemy.orm.exc import NoResultFound
import requests
from datetime import datetime
from sqlalchemy.exc import IntegrityError
import traceback

@pytest.fixture
def mock_session():
    session = MagicMock()
    session.commit = MagicMock()
    session.rollback = MagicMock()
    session.add = MagicMock()
    session.query.return_value.filter_by.return_value.one.side_effect = NoResultFound
    return session

@pytest.fixture
def weather_data():
    return {
        "timelines": {
            "daily": [{"time": "2024-04-26T00:00:00Z", "values": {"temperature": 22, "humidity": 70}}],
            "hourly": [],
            "minutely": []
        }
    }

@patch('tomorrow.db_utils.get_session')
@patch('requests.get')
@patch('tomorrow.config.get_api_key', return_value='fake_api_key')
@patch('tomorrow.config.get_database_url', return_value='fake_db_url')
def test_successful_fetch(mock_get_database_url, mock_get_api_key, mock_get, mock_session, weather_data):
    mock_session.return_value = mock_session
    mock_get.return_value = MagicMock(status_code=200, json=MagicMock(return_value=weather_data))
    from tomorrow.data_fetcher import fetch_data
    fetch_data()
    mock_get.assert_called_once()
    mock_session.commit.assert_called_once()

@patch('tomorrow.db_utils.get_session')
@patch('requests.get', side_effect=requests.exceptions.HTTPError("HTTP Error"))
@patch('tomorrow.config.get_api_key', return_value='fake_api_key')
@patch('tomorrow.config.get_database_url', return_value='fake_db_url')
def test_http_error_handling(mock_get_database_url, mock_get_api_key, mock_get, mock_session):
    mock_session.return_value = mock_session
    from tomorrow.data_fetcher import fetch_data
    fetch_data()
    mock_get.assert_called_once()
    mock_session.rollback.assert_called_once()

@patch('tomorrow.db_utils.get_session')
@patch('requests.get')
@patch('tomorrow.config.get_api_key', return_value='fake_api_key')
@patch('tomorrow.config.get_database_url', return_value='fake_db_url')
def test_fetch_data(mock_get_database_url, mock_get_api_key, mock_get, mock_session):
    mock_session.return_value = mock_session
    weather_data = {
        "timelines": {
            "daily": [
                {"time": "2024-04-26T00:00:00Z", "values": {"temperature": 22, "humidity": 70}},
                {"time": "2024-04-27T00:00:00Z", "values": {"temperature": 23, "humidity": 75}}
            ],
            "hourly": [
                {"time": "2024-04-26T01:00:00Z", "values": {"temperature": 23, "humidity": 72}},
                {"time": "2024-04-26T02:00:00Z", "values": {"temperature": 24, "humidity": 68}}
            ],
            "minutely": [
                {"time": "2024-04-26T00:01:00Z", "values": {"temperature": 22, "humidity": 70}},
                {"time": "2024-04-26T00:02:00Z", "values": {"temperature": 23, "humidity": 72}}
            ]
        }
    }
    mock_get.return_value = MagicMock(status_code=200, json=MagicMock(return_value=weather_data))
    from tomorrow.data_fetcher import fetch_data
    fetch_data()
    mock_get.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.add.assert_called()
    assert mock_session.add.call_count == 4
    assert mock_session.query.call_count == 4
    assert mock_session.query.return_value.filter_by.call_count == 4
    assert mock_session.query.return_value.filter_by.return_value.one.call_count == 4
    assert mock_session.rollback.call_count == 0

@patch('tomorrow.db_utils.get_session')
@patch('requests.get')
@patch('tomorrow.config.get_api_key', return_value='fake_api_key')
@patch('tomorrow.config.get_database_url', return_value='fake_db_url')
def test_fetch_data_integrity_error(mock_get_database_url, mock_get_api_key, mock_get, mock_session):
    mock_session.return_value = mock_session
    weather_data = {
        "timelines": {
            "daily": [
                {"time": "2024-04-26T00:00:00Z", "values": {"temperature": 22, "humidity": 70}},
                {"time": "2024-04-26T00:00:00Z", "values": {"temperature": 23, "humidity": 75}}
            ],
            "hourly": [],
            "minutely": []
        }
    }
    mock_get.return_value = MagicMock(status_code=200, json=MagicMock(return_value=weather_data))
    from tomorrow.data_fetcher import fetch_data
    fetch_data()
    mock_get.assert_called_once()
    mock_session.rollback.assert_called_once()

@patch('tomorrow.db_utils.get_session')
@patch('requests.get')
@patch('tomorrow.config.get_api_key', return_value='fake_api_key')
@patch('tomorrow.config.get_database_url', return_value='fake_db_url')
def test_fetch_data_http_error(mock_get_database_url, mock_get_api_key, mock_get, mock_session):
    mock_session.return_value = mock_session
    mock_get.side_effect = requests.exceptions.HTTPError("HTTP Error")
    from tomorrow.data_fetcher import fetch_data
    fetch_data()
    mock_get.assert_called_once()
    mock_session.rollback.assert_called_once()

@patch('tomorrow.db_utils.get_session')
@patch('requests.get')
@patch('tomorrow.config.get_api_key', return_value='fake_api_key')
@patch('tomorrow.config.get_database_url', return_value='fake_db_url')
def test_fetch_data_exception(mock_get_database_url, mock_get_api_key, mock_get, mock_session):
    mock_session.return_value = mock_session
    mock_get.side_effect = Exception("Some error")
    from tomorrow.data_fetcher import fetch_data
    fetch_data()
    mock_get.assert_called_once()
    mock_session.rollback.assert_called_once()
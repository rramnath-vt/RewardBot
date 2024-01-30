from unittest.mock import Mock
import pytest
from services import leaderboard_service


@pytest.fixture
def mock_ack():
    return Mock()


@pytest.fixture
def mock_body():
    return {"user_id": "123"}


@pytest.fixture
def mock_client():
    return Mock()


@pytest.fixture
def mock_mysql_connection():
    return Mock()


def test_display_leaderboard(mock_ack, mock_body, mock_client, mock_mysql_connection):
    # Initializing the mock objects
    mocker = Mock()
    mocker.patch('mysql_connection.cursor')
    mock_cursor = mock_mysql_connection.cursor.return_value
    mock_cursor.fetchall.return_value = [
        ("Martha", 100), ("Keith", 50), ("Brad", 25)]

    leaderboard_service.display_leaderboard(
        mock_ack, mock_body, mock_client, mock_mysql_connection)

    mock_ack.assert_called_once()
    mock_mysql_connection.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with(
        "SELECT full_name, points FROM employee ORDER BY points DESC LIMIT %s", (10,))
    mock_cursor.fetchall.assert_called_once()
    mock_client.chat_postMessage.assert_called_once_with(
        channel="123",
        blocks=[
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Leaderboard :sports_medal:",
                    "emoji": True
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "🥇 Martha - 100 points",
                    "emoji": True
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "🥈 Keith - 50 points",
                    "emoji": True
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "🥉 Brad - 25 points",
                    "emoji": True
                }
            },
            {
                "type": "divider"
            }
        ]
    )

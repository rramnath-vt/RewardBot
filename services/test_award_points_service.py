import pytest
from datetime import datetime
from unittest.mock import Mock

from services.award_points_service import validate_award


@pytest.fixture
def mock_ack():
    return Mock()


@pytest.fixture
def mock_body():
    return {'user':{"id": "123"}}


@pytest.fixture
def mock_client():
    return Mock()


@pytest.fixture
def mock_mysql_connection():
    return Mock()

@pytest.fixture
def view_state():
    return {
         'state': {'values': {'select_user': {'users_select-action': {'type': 'users_select', 'selected_user': 'U055BA33C9Z'}}, 'award': {'static_select-action': {'type': 'static_select', 'selected_option': {'text': {'type': 'plain_text', 'text': 'Mastermind', 'emoji': True}, 'value': 'mastermind'}}}, 'reward_message': {'message': {'type': 'plain_text_input', 'value': 'dsjfijfsd'}}}}, 'hash': '1683384441.KTbGZTqf', 'title': {'type': 'plain_text', 'text': 'RewardBot', 'emoji': True}, 'clear_on_close': False, 'notify_on_close': False, 'close': {'type': 'plain_text', 'text': 'Cancel', 'emoji': True}, 'submit': {'type': 'plain_text', 'text': 'Submit', 'emoji': True}}

def test_validate_award_success(mock_ack, mock_body, view_state, mock_mysql_connection):
    mocker = Mock()
    mocker.patch('mysql_connection.cursor')
    mock_cursor = mock_mysql_connection.cursor.return_value
    mock_cursor.fetchall.return_value = [
        (1)]

    validate_award(
        mock_ack, mock_body, view_state, mock_mysql_connection)
    mock_cursor.execute.assert_called_once_with(
        "SELECT COUNT(*) FROM audit WHERE awardee = %s AND QUARTER(award_date) = %s", "ramnath", (datetime.now().month+2)//3)
    mock_cursor.fetchall.assert_called_once()


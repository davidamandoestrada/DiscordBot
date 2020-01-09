from data_mappers.registry import DataMapperRegistry
from entities.message import Message
from entities.user import User, find_user_by_user_name, find_users
from freezegun import freeze_time
from main import process_playback


class TestProcessPlayback:
    @classmethod
    def teardown_method(cls):
        DataMapperRegistry().get(Message).flush()
        DataMapperRegistry().get(User).flush()

    @freeze_time("2018-01-01")
    def test_playback_messages(self):
        User.create_new(avatar_url="google.com", user_name="test_user")
        User.create_new(avatar_url="yahoo.com", user_name="test_user_2")

        google_user = find_user_by_user_name("test_user")
        yahoo_user = find_user_by_user_name("test_user_2")

        Message.create_new(author=google_user, content="test_content")
        Message.create_new(author=yahoo_user, content="test_content 2")

        response = process_playback()
        response_message = ['The following is a list of messages that'
                            ' have been recorded:',
                            'User test_user has said:',
                            '2018-01-01 00:00:00: test_content',
                            'User test_user_2 has said:',
                            '2018-01-01 00:00:00: test_content 2']
        assert response['response_message'] == "\n".join(response_message)
        assert response['error'] is None

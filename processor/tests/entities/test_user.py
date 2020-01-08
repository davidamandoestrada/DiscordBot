from data_mappers.registry import DataMapperRegistry
from entities.message import Message
from entities.user import User, find_user_by_user_name, find_users


class TestUser:
    @classmethod
    def teardown_method(cls):
        DataMapperRegistry().get(Message).flush()
        DataMapperRegistry().get(User).flush()

    def test_create_users_and_find_all_of_them(self):
        User.create_new(avatar_url="google.com", user_name="test_user")
        User.create_new(avatar_url="yahoo.com", user_name="test_user_2")
        users = find_users()

        assert len(users) == 2

    def test_find_user_and_has_fields_populated(self):
        User.create_new(avatar_url="google.com", user_name="test_user")
        user = find_user_by_user_name("test_user")

        assert user.avatar_url == "google.com"
        assert user.user_name == "test_user"

    def test_create_user_and_find_their_messages(self):
        User.create_new(avatar_url="google.com", user_name="test_user")
        user = find_user_by_user_name("test_user")
        Message.create_new(author=user, content="test_content")
        Message.create_new(author=user, content="test_content 2")

        messages = user.messages

        assert len(messages) == 2

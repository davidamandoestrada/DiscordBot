from data_mappers.registry import DataMapperRegistry
from entities.message import Message, find_messages_by_user
from entities.user import User


class TestMessage:
    @classmethod
    def teardown_method(cls):
        DataMapperRegistry().get(Message).flush()
        DataMapperRegistry().get(User).flush()

    def test_create_one_new_message_and_find_it(self):
        user = User(_id=1, avatar_url="google.com", user_name="test_user")
        Message.create_new(author=user, content="test_content")
        messages = find_messages_by_user(user)

        assert len(messages) == 1

    def test_message_fields_will_be_populated_correctly(self):
        user = User(_id=1, avatar_url="google.com", user_name="test_user")
        Message.create_new(author=user, content="test_content")
        messages = find_messages_by_user(user)

        assert messages[0].author_id == user._id
        assert messages[0].content == "test_content"

    def test_create_multiple_new_messages_by_user_and_find_them(self):
        user = User(_id=1, avatar_url="google.com", user_name="test_user")
        Message.create_new(author=user, content="test_content")
        Message.create_new(author=user, content="test_content 2")
        messages = find_messages_by_user(user)

        assert len(messages) == 2

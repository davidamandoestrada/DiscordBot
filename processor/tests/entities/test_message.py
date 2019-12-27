import pytest

from entities.message import Message, find_messages_by_user
from entities.user import User


class TestMessage:
    # def test_create_new_message_and_find_it(self):
    #     user = User(id=1, user_name="test_user")
    #     Message.create_new(author=user, content="test_content")
    #     messages = find_messages_by_user(user)

    #     print(messages)
    #     assert len(messages) == 1
    #     assert messages[0].author_id == user.id
    #     assert messages[0].content == "test_content"

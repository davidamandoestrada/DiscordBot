from datetime import datetime

from data_mappers.registry import DataMapperRegistry


def find_messages_by_user(user):
    message_data_mapper = DataMapperRegistry().get(Message)
    messages = message_data_mapper.find_messages_by_user(user)
    return messages


class Message:
    def __init__(self, _id, author_id, date_time, content: str):
        self._id = _id
        self.author_id = author_id
        self.date_time = date_time
        self.content = content

    @classmethod
    def create_new(cls, author, content: str):
        message_data_mapper = DataMapperRegistry().get(cls)
        message_data_mapper.create(author, datetime.now(), content)

from dataclasses import dataclass
from datetime import datetime
from typing import List

from data_mappers.registry import DataMapperRegistry
from entities.base import BaseEntity


@dataclass(init=False)
class Message(BaseEntity):
    _id: int
    author_id: int
    date_time: datetime
    content: str

    def __init__(self,
                 _id: int,
                 author_id: int,
                 date_time: datetime,
                 content: str):
        self._id = _id
        self.author_id = author_id
        self.date_time = date_time
        self.content = content

        super(Message, self).__init__()

    @classmethod
    def create_new(cls, author, content: str) -> None:
        message_data_mapper = DataMapperRegistry().get(cls)
        message_data_mapper.create(author, datetime.now(), content)


def find_messages_by_user(user) -> List[Message]:
    message_data_mapper = DataMapperRegistry().get(Message)
    messages = message_data_mapper.find_messages_by_user(user)
    return messages

from dataclasses import dataclass
from math import ceil, exp, floor, log
from typing import List, Optional

from data_mappers.registry import DataMapperRegistry
from entities.base import BaseEntity
from entities.message import find_messages_by_user


@dataclass(init=False)
class User(BaseEntity):
    _id: int
    user_name: str
    avatar_url: str

    def __init__(self, _id: int, user_name: str, avatar_url: str):
        self._id = _id
        self.user_name = user_name
        self.avatar_url = avatar_url

        super(User, self).__init__()

    @classmethod
    def create_new(cls, user_name: str, avatar_url: Optional[str] = None):
        user_data_mapper = DataMapperRegistry().get(cls)
        user_data_mapper.create(user_name, avatar_url)

    @property
    def messages(self):
        return find_messages_by_user(self)

    @property
    def exp(self):
        return len(self.messages)

    @property
    def level(self):
        if self.exp > 0:
            return floor(log(self.exp))
        else:
            return 0

    def exp_for_level(self, level: int):
        return ceil(exp(level))


class UserNotFoundError(Exception):
    """Raised when the user does not exist"""

    pass


def find_users() -> List[User]:
    user_data_mapper = DataMapperRegistry().get(User)
    users = user_data_mapper.find_users()
    return users


def find_user_by_user_name(user_name: str) -> User:
    user_data_mapper = DataMapperRegistry().get(User)
    user = user_data_mapper.find_user_by_user_name(user_name)
    return user

from data_mappers.registry import DataMapperRegistry
from entities.base import BaseEntity
from entities.message import find_messages_by_user


def find_users():
    user_data_mapper = DataMapperRegistry().get(User)
    users = user_data_mapper.find_users()
    return users


def find_user_by_user_name(user_name: str):
    user_data_mapper = DataMapperRegistry().get(User)
    user = user_data_mapper.find_user_by_user_name(user_name)
    return user


class User(BaseEntity):
    def __init__(self, _id, user_name: str, avatar_url: str):
        self._id = _id
        self.user_name = user_name
        self.avatar_url = avatar_url

        super(User, self).__init__()

    @classmethod
    def create_new(cls, user_name: str, avatar_url: str):
        user_data_mapper = DataMapperRegistry().get(cls)
        user_data_mapper.create(user_name, avatar_url)

    @property
    def messages(self):
        return find_messages_by_user(self)


class UserNotFoundError(Exception):
    """Raised when the user does not exist"""

    pass

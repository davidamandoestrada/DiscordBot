from data_mappers.registry import DataMapperRegistry
from entities.message import find_messages_by_user_name


def find_users():
    user_data_mapper = DataMapperRegistry().get(User)
    users = user_data_mapper.find_users()
    return users


def find_user_by_user_name(user_name: str):
    user_data_mapper = DataMapperRegistry().get(User)
    user = user_data_mapper.find_user_by_user_name(user_name)
    return user


class User:
    def __init__(self, user_name: str):
        self.user_name = user_name

    @classmethod
    def create_new(cls, user_name: str):
        user_data_mapper = DataMapperRegistry().get(cls)
        user_data_mapper.create(user_name)

    @property
    def messages(self):
        return find_messages_by_user_name(self.user_name)


class UserNotFoundError(Exception):
    """Raised when the user does not exist"""

    pass

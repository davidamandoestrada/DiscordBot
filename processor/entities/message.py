from data_mappers.registry import DataMapperRegistry


def find_messages_by_user_name(user_name: str):
    user_data_mapper = DataMapperRegistry().get(Message)
    user = user_data_mapper.find_messages_by_user_name(user_name)
    return user


class Message:
    def __init__(self, author: str, content: str):
        self.author = author
        self.content = content

    @classmethod
    def create_new(cls, author: str, content: str):
        message_data_mapper = DataMapperRegistry().get(cls)
        message_data_mapper.create(author, content)

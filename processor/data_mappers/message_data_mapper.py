import pugsql
from data_mappers.data_mapper import DataMapper, InMemoryDataMapper
from entities.message import Message

# Create a module of database functions from a set of sql files on disk.
queries = pugsql.module("resources/sql/message")

# Point the module at your database.
queries.connect("postgresql://postgres@db/discordbot")


class InMemoryMessageDataMapper(InMemoryDataMapper):
    entities = {}
    current_id = 1

    def create(self, user, date_time, content: str):
        if user.user_name not in self.entities:
            self.entities[user.user_name] = []
        self.entities[user.user_name].append(
            Message(
                _id=self.current_id,
                date_time=date_time,
                content=content,
                author_id=user._id,
            )
        )

    def find_messages_by_user(self, user):
        return self.entities.get(user.user_name, [])


class MessageDataMapper(DataMapper):
    def create(self, user, date_time, content: str):
        queries.insert_message(user_id=user._id, date_time=date_time, content=content)

    def find_messages_by_user(self, user):
        results = queries.find_messages_by_user_id(user_id=user._id)
        return [
            Message(
                _id=result["id"],
                date_time=result["date_time"],
                content=result["content"],
                author_id=result["user_id"],
            )
            for result in results
        ]

import pugsql

from entities.message import Message


# Create a module of database functions from a set of sql files on disk.
queries = pugsql.module("resources/sql/message")

# Point the module at your database.
queries.connect("postgresql://postgres@db/discordbot")


class MessageDataMapper:
    def create(self, author: str, content: str):
        queries.insert_message(user_name=author, content=content)

    def find_messages_by_user_name(self, user_name: str):
        results = queries.find_messages_by_user_name(user_name=user_name)
        return [
            Message(content=result["content"], author=result["user_name"])
            for result in results
        ]

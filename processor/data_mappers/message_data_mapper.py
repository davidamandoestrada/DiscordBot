import pugsql

from entities.message import Message


# Create a module of database functions from a set of sql files on disk.
queries = pugsql.module("resources/sql")

# Point the module at your database.
queries.connect("postgresql://postgres@db")


class MessageDataMapper:
    def create(self, author: str, content: str):
        pass

    def find_messages_by_user_name(self, user_name: str):
        return [
            Message(author="Dave", content="Test"),
            Message(author="Dave", content="Test"),
        ]

import pugsql

from entities.message import Message


# Create a module of database functions from a set of sql files on disk.
queries = pugsql.module("resources/sql/message")

# Point the module at your database.
queries.connect("postgresql://postgres@db/discordbot")


class InMemoryMessageDataMapper:
    messages = {}
    current_id = 1

    def create(self, user, date_time, content: str):
        if user.user_name not in self.messages:
            self.messages[user.user_name] = []
        self.messages[user.user_name].append(
            Message(
                id=self.current_id,
                date_time=date_time,
                content=content,
                author_id=user.id,
            )
        )

    def find_messages_by_user(self, user):
        return self.messages.get(user.user_name, [])


class MessageDataMapper:
    def create(self, user, date_time, content: str):
        queries.insert_message(user_id=user.id, date_time=date_time, content=content)

    def find_messages_by_user(self, user):
        results = queries.find_messages_by_user_id(user_id=user.id)
        return [
            Message(
                id=result["id"],
                date_time=result["date_time"],
                content=result["content"],
                author_id=result["user_id"],
            )
            for result in results
        ]

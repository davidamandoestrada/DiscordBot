import pugsql

from entities.user import User, UserNotFoundError

# Create a module of database functions from a set of sql files on disk.
queries = pugsql.module("resources/sql/user")

# Point the module at your database.
queries.connect("postgresql://postgres@db/discordbot")


class UserDataMapper:
    def create(self, user_name: str, avatar_url: str):
        queries.insert_user(user_name=user_name, avatar_url=avatar_url)

    def update(self, user):
        queries.update_user(
            id=user.id, user_name=user.user_name, avatar_url=user.avatar_url
        )

    def find_users(self):
        results = queries.find_users()
        return [
            User(
                id=result["id"],
                user_name=result["user_name"],
                avatar_url=result["avatar_url"],
            )
            for result in results
        ]

    def find_user_by_user_name(self, user_name: str):
        result = queries.find_user_by_user_name(user_name=user_name)
        if result:
            return User(
                id=result["id"],
                user_name=result["user_name"],
                avatar_url=result["avatar_url"],
            )
        else:
            raise UserNotFoundError

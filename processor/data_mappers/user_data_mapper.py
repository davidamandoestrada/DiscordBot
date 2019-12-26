import pugsql

from entities.user import User, UserNotFoundError

# Create a module of database functions from a set of sql files on disk.
queries = pugsql.module("resources/sql/user")

# Point the module at your database.
queries.connect("postgresql://postgres@db/discordbot")


class UserDataMapper:
    def create(self, user_name: str):
        queries.insert_user(user_name=user_name)

    def find_users(self):
        results = queries.find_users()
        return [User(result["user_name"]) for result in results]

    def find_user_by_user_name(self, user_name: str):
        result = queries.find_user_by_user_name(user_name=user_name)
        if result:
            return User(user_name=result["user_name"])
        else:
            raise UserNotFoundError

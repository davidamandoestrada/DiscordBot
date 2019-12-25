import pugsql

from entities.user import User

# Create a module of database functions from a set of sql files on disk.
queries = pugsql.module("resources/sql")

# Point the module at your database.
queries.connect("postgresql://postgres@db")


class UserDataMapper:
    def create(self):
        pass

    def find_users(self):
        return [User(user_name="Dave#6945"), User(user_name="Niltze#4073")]

    def find_user_by_user_name(self, user_name: str):
        return User(user_name=user_name)

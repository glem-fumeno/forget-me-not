from api.database.operation import DatabaseOperation


class UserSelectUserIdByEmailOperation(DatabaseOperation):
    def run(self, email: str) -> int | None: ...

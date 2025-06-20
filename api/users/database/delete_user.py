from api.database.operation import DatabaseOperation


class UserDeleteUserOperation(DatabaseOperation):
    def run(self, user_id: int):
        self.cursor.execute(self.query, (user_id,))

    @property
    def query(self) -> str:
        return """
            DELETE FROM users_ WHERE user_id_ = ?
        """

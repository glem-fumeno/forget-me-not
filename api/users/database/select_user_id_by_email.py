from api.database.operation import DatabaseOperation


class UserSelectUserIdByEmailOperation(DatabaseOperation):
    def run(self, email: str) -> int | None:
        result = self.cursor.execute(self.query, (email,))
        columns = result.fetchone()
        if columns is None:
            return
        return columns[0]

    @property
    def query(self) -> str:
        return """
            SELECT user_id_ FROM users_ WHERE email_ = ?
        """

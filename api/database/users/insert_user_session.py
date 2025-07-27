from api.database.operation import DatabaseOperation


class UserInsertUserSessionOperation(DatabaseOperation):
    def run(self, user_id: int, token: str):
        self.cursor.execute(self.query, (user_id, token))

    @property
    def query(self) -> str:
        return """
            INSERT INTO users_sessions_ (user_id_, token_)
            VALUES (?, ?)
        """

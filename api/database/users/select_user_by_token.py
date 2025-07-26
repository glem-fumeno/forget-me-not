from api.database.operation import DatabaseOperation
from api.models.users.models import UserModel


class UserSelectUserByTokenOperation(DatabaseOperation):
    def run(self, token: str) -> UserModel | None:
        result = self.cursor.execute(self.query, (token,))
        columns = result.fetchone()
        if columns is None:
            return
        return UserModel.from_db(result.description, columns)

    @property
    def query(self) -> str:
        return """
            SELECT user_id_, cart_id_, username_, email_, password_, role_
            FROM users_
            INNER JOIN users_sessions_ USING (user_id_)
            WHERE token_ = ?
        """

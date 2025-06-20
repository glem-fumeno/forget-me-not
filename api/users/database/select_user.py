from api.database.operation import DatabaseOperation
from api.users.schemas.models import UserModel


class UserSelectUserOperation(DatabaseOperation):
    def run(self, user_id: int) -> UserModel | None:
        result = self.cursor.execute(self.query, (user_id,))
        columns = result.fetchone()
        if columns is None:
            return
        return UserModel(*columns)

    @property
    def query(self) -> str:
        return """
            SELECT user_id_, username_, email_, password_
            FROM users_
            WHERE user_id_ = ?
        """

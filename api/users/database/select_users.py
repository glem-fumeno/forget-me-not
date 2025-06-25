from api.database.operation import DatabaseOperation
from api.users.schemas.models import UserModel


class UserSelectUsersOperation(DatabaseOperation):
    def run(self) -> dict[int, UserModel]:
        result = self.cursor.execute(self.query)
        results = result.fetchall()
        return {
            columns[0]: UserModel.from_db(result.description, columns)
            for columns in results
        }

    @property
    def query(self) -> str:
        return """
            SELECT user_id_, username_, email_, password_, role_
            FROM users_
        """

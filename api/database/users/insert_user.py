from api.database.operation import DatabaseOperation
from api.models.users.models import UserModel


class UserInsertUserOperation(DatabaseOperation):
    def run(self, model: UserModel):
        result = self.cursor.execute(self.query, model.parameters)
        assert result.lastrowid is not None, "could not insert user"
        model.user_id = result.lastrowid

    @property
    def query(self) -> str:
        return """
            INSERT INTO users_ (username_, email_, password_, role_)
            VALUES (?, ?, ?, ?)
        """

from api.database.operation import DatabaseOperation
from api.users.schemas.models import UserModel


class UserUpdateUserOperation(DatabaseOperation):
    def run(self, model: UserModel):
        self.cursor.execute(self.query, (*model.parameters, model.user_id))

    @property
    def query(self) -> str:
        return """
            UPDATE users_
            SET
                username_ = ?,
                email_ = ?,
                password_ = ?,
                role_ = ?
            WHERE
                user_id_ = ?
        """

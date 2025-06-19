from api.database.operation import DatabaseOperation
from api.users.schemas.models import UserModel


class UserInsertUserOperation(DatabaseOperation):
    def run(self, model: UserModel):
        user_id = self.cursor.execute(
            self.__user_insert_query,
            (model.username, model.email, model.password),
        ).fetchone()
        model.user_id = user_id

    @property
    def __user_insert_query(self) -> str:
        return """
            INSERT INTO users_
                (username_, email_, password_)
            VALUES
                (?, ?, ?)
            RETURNING user_id_
        """

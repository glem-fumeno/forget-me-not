from api.database.operation import DatabaseOperation
from api.users.schemas.models import UserSessionModel


class UserInsertUserSessionOperation(DatabaseOperation):
    def run(self, model: UserSessionModel):
        self.cursor.execute(self.query, model.parameters)

    @property
    def query(self) -> str:
        return """
            INSERT INTO users_sessions_ (user_id_, token_)
            VALUES (?, ?)
        """

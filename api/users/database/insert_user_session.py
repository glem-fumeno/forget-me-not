from api.database.operation import DatabaseOperation
from api.users.schemas.models import UserModel, UserSessionModel


class UserInsertUserSessionOperation(DatabaseOperation):
    def run(self, model: UserSessionModel): ...

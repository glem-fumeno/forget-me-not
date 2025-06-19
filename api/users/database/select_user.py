from api.database.operation import DatabaseOperation
from api.users.schemas.models import UserModel


class UserSelectUserOperation(DatabaseOperation):
    def run(self, user_id: int) -> UserModel | None: ...

from api.database.repository import DatabaseRepository
from api.users.database.delete_user import UserDeleteUserOperation
from api.users.database.insert_user import UserInsertUserOperation
from api.users.database.insert_user_session import (
    UserInsertUserSessionOperation,
)
from api.users.database.select_user import UserSelectUserOperation
from api.users.database.select_user_id_by_email import (
    UserSelectUserIdByEmailOperation,
)
from api.users.database.update_user import UserUpdateUserOperation
from api.users.schemas.models import UserModel, UserSessionModel


class UserDatabaseRepository(DatabaseRepository):
    def insert_user(self, model: UserModel):
        return UserInsertUserOperation(self.cursor).run(model)

    def insert_user_session(self, model: UserSessionModel):
        return UserInsertUserSessionOperation(self.cursor).run(model)

    def select_user(self, user_id: int) -> UserModel | None:
        return UserSelectUserOperation(self.cursor).run(user_id)

    def select_user_id_by_email(self, email: str) -> int | None:
        return UserSelectUserIdByEmailOperation(self.cursor).run(email)

    def update_user(self, model: UserModel):
        return UserUpdateUserOperation(self.cursor).run(model)

    def delete_user(self, user_id: int):
        return UserDeleteUserOperation(self.cursor).run(user_id)

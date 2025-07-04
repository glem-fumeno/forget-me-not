from api.database.repository import DatabaseRepository
from api.users.database.delete_user import UserDeleteUserOperation
from api.users.database.insert_user import UserInsertUserOperation
from api.users.database.insert_user_session import (
    UserInsertUserSessionOperation,
)
from api.users.database.select_user import UserSelectUserOperation
from api.users.database.select_user_by_token import (
    UserSelectUserByTokenOperation,
)
from api.users.database.select_user_id_by_email import (
    UserSelectUserIdByEmailOperation,
)
from api.users.database.select_users import UserSelectUsersOperation
from api.users.database.update_user import UserUpdateUserOperation
from api.users.schemas.models import UserModel, UserSessionModel


class UserDatabaseRepository(DatabaseRepository):
    def insert_user(self, model: UserModel):
        return UserInsertUserOperation(self.ctx, self.cursor).run(model)

    def insert_user_session(self, model: UserSessionModel):
        return UserInsertUserSessionOperation(self.ctx, self.cursor).run(model)

    def select_user(self, user_id: int) -> UserModel | None:
        return UserSelectUserOperation(self.ctx, self.cursor).run(user_id)

    def select_users(self) -> dict[int, UserModel]:
        return UserSelectUsersOperation(self.ctx, self.cursor).run()

    def select_user_id_by_email(self, email: str) -> int | None:
        return UserSelectUserIdByEmailOperation(self.ctx, self.cursor).run(
            email
        )

    def select_user_by_token(self, token: str) -> UserModel | None:
        return UserSelectUserByTokenOperation(self.ctx, self.cursor).run(token)

    def update_user(self, model: UserModel):
        return UserUpdateUserOperation(self.ctx, self.cursor).run(model)

    def delete_user(self, user_id: int):
        return UserDeleteUserOperation(self.ctx, self.cursor).run(user_id)

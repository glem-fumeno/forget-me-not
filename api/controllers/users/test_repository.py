from api.controllers.test_repository import TestRepository
from api.models.users.models import UserModel, UserSessionModel


class UserTestRepository(TestRepository):
    def init_users(self):
        self.max_user_id: int = 0
        self.user_map: dict[int, UserModel] = {}
        self.email_map: dict[str, int] = {}
        self.user_login_map: dict[str, int] = {}

    def insert_user(self, model: UserModel):
        self.max_user_id += 1
        self.user_map[self.max_user_id] = model
        self.email_map[model.email] = self.max_user_id
        model.user_id = self.max_user_id

    def insert_user_session(self, model: UserSessionModel):
        self.user_login_map[model.token] = model.user_id

    def select_user(self, user_id: int) -> UserModel | None:
        result = self.user_map.get(user_id)
        if result is None:
            return
        return result.copy()

    def select_users(self) -> dict[int, UserModel]:
        return self.user_map

    def select_user_id_by_email(self, email: str) -> int | None:
        return self.email_map.get(email)

    def select_user_by_token(self, token: str) -> UserModel | None:
        user_id = self.user_login_map.get(token)
        if user_id is None:
            return
        return self.user_map[user_id]

    def update_user(self, model: UserModel):
        old_model = self.user_map[model.user_id]
        self.user_map[model.user_id] = model
        self.email_map.pop(old_model.email, -1)
        self.email_map[model.email] = model.user_id

    def delete_user(self, user_id: int):
        result = self.user_map.pop(user_id, None)
        if result is None:
            return
        self.email_map.pop(result.email, None)

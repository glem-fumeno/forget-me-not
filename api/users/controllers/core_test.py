from api.users.common import get_hash, get_uuid
from api.users.schemas.models import RoleLiteral, UserModel, UserSessionModel


class UserTestRepository:
    def __init__(self) -> None:
        super().__init__()
        self.init_users()

    def init_users(self):
        self.max_user_id: int = 0
        self.user_map: dict[int, UserModel] = {}
        self.email_map: dict[str, int] = {}
        self.user_login_map: dict[str, int] = {}

        self.__insert_user(
            "aanderson", "alice.anderson@example.com", "A1ice_89rocks", "admin"
        )
        self.__insert_user(
            "b.baker92", "bob.baker@example.com", "SunsetDrive@34", "user"
        )

    def login(self, user_id: int):
        token = get_uuid()
        self.user_login_map[token] = user_id
        return token

    def __insert_user(
        self, username: str, email: str, password: str, role: RoleLiteral
    ):
        self.max_user_id += 1
        self.user_map[self.max_user_id] = UserModel(
            self.max_user_id, username, email, get_hash(password), role
        )
        self.email_map[email] = self.max_user_id

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

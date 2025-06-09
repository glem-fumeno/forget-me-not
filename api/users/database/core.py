from api.database import DatabaseConnector
from api.singleton import Singleton
from api.users.schemas.models import UserModel, UserSessionModel


class UserDatabaseRepository(DatabaseConnector, metaclass=Singleton):
    def __init__(self) -> None:
        super().__init__()
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
        return self.user_map.get(user_id)

    def select_user_id_by_email(self, email: str) -> int | None:
        return self.email_map.get(email)

from typing import Protocol

from api.controller import Controller, Repository
from api.users.schemas.models import UserModel, UserSessionModel


class UserRepository(Repository, Protocol):
    def insert_user(self, model: UserModel): ...
    def insert_user_session(self, model: UserSessionModel): ...
    def select_user(self, user_id: int) -> UserModel | None: ...
    def select_user_id_by_email(self, email: str) -> int | None: ...

class UserController(Controller):
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository
        super().__init__()

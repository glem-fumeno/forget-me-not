from typing import Protocol

from api.context import Context
from api.controller import Controller, Repository
from api.errors import Inaccessible, LoggedOut
from api.items.schemas.models import ItemModel, ItemUserModel
from api.users.schemas.models import UserModel


class ItemRepository(Repository, Protocol):
    def insert_item(self, model: ItemModel): ...
    def insert_item_user(self, model: ItemUserModel): ...
    def select_user_by_token(self, token: str) -> UserModel | None: ...
    def select_item(self, item_id: int) -> ItemModel | None: ...
    def select_item_by_name(self, name: str) -> int | None: ...
    def update_item(self, model: ItemModel): ...
    def delete_item(self, item_id: int): ...


class ItemController(Controller):
    def __init__(self, ctx: Context, repository: ItemRepository) -> None:
        self.repository = repository
        super().__init__(ctx)

    def validate_access(self, admin: bool = True):
        issuer = self.repository.select_user_by_token(
            self.ctx.get("token", "")
        )
        if issuer is None:
            raise LoggedOut
        if admin and issuer.role != "admin":
            raise Inaccessible

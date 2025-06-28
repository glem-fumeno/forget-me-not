from typing import Protocol

from api.context import Context
from api.controller import Controller, Repository
from api.errors import LoggedOut
from api.items.schemas.models import ItemModel
from api.recipes.schemas.models import RecipeModel, RecipeUserModel
from api.users.schemas.models import UserModel


class RecipeRepository(Repository, Protocol):
    def insert_recipe(self, user_id: int, model: RecipeModel): ...
    def insert_recipe_user(self, model: RecipeUserModel): ...
    def insert_recipe_item(self, recipe_id: int, item_id: int): ...
    def select_items(self) -> dict[int, ItemModel]: ...
    def select_recipes(self, user_id: int) -> dict[int, RecipeModel]: ...
    def select_recipe_items(self, recipe_id: int) -> list[ItemModel]: ...
    def select_recipe(
        self, user_id: int, recipe_id: int
    ) -> RecipeModel | None: ...
    def select_user_by_token(self, token: str) -> UserModel | None: ...
    def update_recipe(self, model: RecipeModel): ...
    def delete_recipe(self, recipe_id: int): ...
    def delete_recipe_item(self, recipe_id: int, item_id: int): ...


class RecipeController(Controller):
    def __init__(self, ctx: Context, repository: RecipeRepository) -> None:
        self.repository = repository
        super().__init__(ctx, repository)

    def validate_access(self):
        issuer = self.repository.select_user_by_token(
            self.ctx.get("token", "")
        )
        if issuer is None:
            raise LoggedOut
        self.issuer = issuer

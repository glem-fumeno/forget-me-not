from api.database.repository import DatabaseRepository
from api.database.items.select_items import ItemSelectItemsOperation
from api.models.items.models import ItemModel
from api.database.recipes.delete_recipe import RecipeDeleteRecipeOperation
from api.database.recipes.delete_recipe_item import (
    RecipeDeleteRecipeItemOperation,
)
from api.database.recipes.insert_recipe import RecipeInsertRecipeOperation
from api.database.recipes.insert_recipe_item import (
    RecipeInsertRecipeItemOperation,
)
from api.database.recipes.insert_recipe_user import (
    RecipeInsertRecipeUserOperation,
)
from api.database.recipes.select_recipe import RecipeSelectRecipeOperation
from api.database.recipes.select_recipe_items import (
    RecipeSelectRecipeItemsOperation,
)
from api.database.recipes.select_recipes import RecipeSelectRecipesOperation
from api.database.recipes.update_recipe import RecipeUpdateRecipeOperation
from api.models.recipes.models import RecipeModel, RecipeUserModel
from api.database.users.select_user_by_token import (
    UserSelectUserByTokenOperation,
)
from api.models.users.models import UserModel


class RecipeDatabaseRepository(DatabaseRepository):
    def insert_recipe(self, user_id: int, model: RecipeModel):
        return RecipeInsertRecipeOperation(self.ctx, self.cursor).run(
            user_id, model
        )

    def insert_recipe_user(self, model: RecipeUserModel):
        return RecipeInsertRecipeUserOperation(self.ctx, self.cursor).run(
            model
        )

    def insert_recipe_item(self, recipe_id: int, item_id: int):
        return RecipeInsertRecipeItemOperation(self.ctx, self.cursor).run(
            recipe_id, item_id
        )

    def select_items(self) -> dict[int, ItemModel]:
        return ItemSelectItemsOperation(self.ctx, self.cursor).run()

    def select_recipes(self, user_id: int) -> dict[int, RecipeModel]:
        return RecipeSelectRecipesOperation(self.ctx, self.cursor).run(user_id)

    def select_recipe_items(self, recipe_id: int) -> list[ItemModel]:
        return RecipeSelectRecipeItemsOperation(self.ctx, self.cursor).run(
            recipe_id
        )

    def select_recipe(
        self, user_id: int, recipe_id: int
    ) -> RecipeModel | None:
        return RecipeSelectRecipeOperation(self.ctx, self.cursor).run(
            user_id, recipe_id
        )

    def select_user_by_token(self, token: str) -> UserModel | None:
        return UserSelectUserByTokenOperation(self.ctx, self.cursor).run(token)

    def update_recipe(self, model: RecipeModel):
        return RecipeUpdateRecipeOperation(self.ctx, self.cursor).run(model)

    def delete_recipe(self, recipe_id: int):
        return RecipeDeleteRecipeOperation(self.ctx, self.cursor).run(
            recipe_id
        )

    def delete_recipe_item(self, recipe_id: int, item_id: int):
        return RecipeDeleteRecipeItemOperation(self.ctx, self.cursor).run(
            recipe_id, item_id
        )

import inspect
from typing import Any

from api.database.carts.delete_cart import CartDeleteCartOperation
from api.database.carts.delete_cart_item import CartDeleteCartItemOperation
from api.database.carts.insert_cart import CartInsertCartOperation
from api.database.carts.insert_cart_items import CartInsertCartItemsOperation
from api.database.carts.insert_cart_user import CartInsertCartUserOperation
from api.database.carts.select_cart import CartSelectCartOperation
from api.database.carts.select_cart_items import CartSelectCartItemsOperation
from api.database.carts.select_carts import CartSelectCartsOperation
from api.database.carts.update_cart import CartUpdateCartOperation
from api.database.connector import DatabaseConnector
from api.database.items.delete_item import ItemDeleteItemOperation
from api.database.items.insert_item import ItemInsertItemOperation
from api.database.items.insert_item_user import ItemInsertItemUserOperation
from api.database.items.select_by_name_item import (
    ItemSelectItemByNameOperation,
)
from api.database.items.select_item import ItemSelectItemOperation
from api.database.items.select_items import ItemSelectItemsOperation
from api.database.items.update_item import ItemUpdateItemOperation
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
from api.database.users.delete_user import UserDeleteUserOperation
from api.database.users.insert_user import UserInsertUserOperation
from api.database.users.insert_user_session import (
    UserInsertUserSessionOperation,
)
from api.database.users.select_user import UserSelectUserOperation
from api.database.users.select_user_by_token import (
    UserSelectUserByTokenOperation,
)
from api.database.users.select_user_id_by_email import (
    UserSelectUserIdByEmailOperation,
)
from api.database.users.select_users import UserSelectUsersOperation
from api.database.users.update_user import UserUpdateUserOperation


class DatabaseRepository(DatabaseConnector):
    insert_user = UserInsertUserOperation.run
    insert_user_session = UserInsertUserSessionOperation.run
    select_user = UserSelectUserOperation.run
    select_users = UserSelectUsersOperation.run
    select_user_id_by_email = UserSelectUserIdByEmailOperation.run
    select_user_by_token = UserSelectUserByTokenOperation.run
    update_user = UserUpdateUserOperation.run
    delete_user = UserDeleteUserOperation.run

    insert_item = ItemInsertItemOperation.run
    insert_item_user = ItemInsertItemUserOperation.run
    select_items = ItemSelectItemsOperation.run
    select_item = ItemSelectItemOperation.run
    select_user_by_token = UserSelectUserByTokenOperation.run
    select_item_by_name = ItemSelectItemByNameOperation.run
    update_item = ItemUpdateItemOperation.run
    delete_item = ItemDeleteItemOperation.run

    insert_recipe = RecipeInsertRecipeOperation.run
    insert_recipe_user = RecipeInsertRecipeUserOperation.run
    insert_recipe_item = RecipeInsertRecipeItemOperation.run
    select_items = ItemSelectItemsOperation.run
    select_recipes = RecipeSelectRecipesOperation.run
    select_recipe_items = RecipeSelectRecipeItemsOperation.run
    select_recipe = RecipeSelectRecipeOperation.run
    select_user_by_token = UserSelectUserByTokenOperation.run
    update_recipe = RecipeUpdateRecipeOperation.run
    delete_recipe = RecipeDeleteRecipeOperation.run
    delete_recipe_item = RecipeDeleteRecipeItemOperation.run

    insert_cart = CartInsertCartOperation.run
    insert_cart_user = CartInsertCartUserOperation.run
    insert_cart_items = CartInsertCartItemsOperation.run
    select_items = ItemSelectItemsOperation.run
    select_carts = CartSelectCartsOperation.run
    select_cart_items = CartSelectCartItemsOperation.run
    select_cart = CartSelectCartOperation.run
    select_user_by_token = UserSelectUserByTokenOperation.run
    update_cart = CartUpdateCartOperation.run
    delete_cart = CartDeleteCartOperation.run
    delete_cart_item = CartDeleteCartItemOperation.run

    def __getattribute__(self, name: str, /) -> Any:
        field = object.__getattribute__(self, name)
        if (
            callable(field)
            and hasattr(field, "__qualname__")
            and field.__name__ == "run"
        ):
            r = inspect.getmodule(field)
            classname = field.__qualname__.removesuffix(".run")
            return getattr(r, classname)(self.ctx, self.cursor).run
        return field

from api.context import Context
from api.controllers.carts.controllers import CartControllers
from api.controllers.items.controllers import ItemControllers
from api.controllers.recipes.controllers import RecipeControllers
from api.database.repository import DatabaseRepository


class Controllers:
    items: ItemControllers
    recipes: RecipeControllers
    carts: CartControllers

    def __init__(self, ctx: Context, repository: DatabaseRepository) -> None:
        self.ctx = ctx
        self.repository = repository
        self.items = ItemControllers(ctx, repository)
        self.recipes = RecipeControllers(ctx, repository)
        self.carts = CartControllers(ctx, repository)

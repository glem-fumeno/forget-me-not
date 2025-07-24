from api.context import Context
from api.controllers.carts.controllers import CartControllers
from api.controllers.items.controllers import ItemControllers
from api.controllers.recipes.controllers import RecipeControllers
from api.controllers.repository import Repository
from api.controllers.users.controllers import UserControllers


class Controllers:
    users: UserControllers
    items: ItemControllers
    recipes: RecipeControllers
    carts: CartControllers

    def __init__(self, ctx: Context, repository: Repository) -> None:
        self.ctx = ctx
        self.repository = repository
        self.users = UserControllers(ctx, repository)
        self.items = ItemControllers(ctx, repository)
        self.recipes = RecipeControllers(ctx, repository)
        self.carts = CartControllers(ctx, repository)

from api.database.carts.repository import CartRepository
from api.database.connector import DatabaseConnector
from api.database.items.repository import ItemRepository
from api.database.recipes.repository import RecipeRepository
from api.database.users.repository import UserRepository


class DatabaseRepository(DatabaseConnector):
    users: UserRepository
    items: ItemRepository
    recipes: RecipeRepository
    carts: CartRepository

    def __enter__(self):
        super().__enter__()
        self.users = UserRepository(self.ctx, self.cursor)
        self.items = ItemRepository(self.ctx, self.cursor)
        self.recipes = RecipeRepository(self.ctx, self.cursor)
        self.carts = CartRepository(self.ctx, self.cursor)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self.carts, self.recipes, self.items, self.users
        super().__exit__(exc_type, exc_val, exc_tb)

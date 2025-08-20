from api.database.carts.repository import CartRepository
from api.database.connector import DatabaseConnector
from api.database.items.repository import ItemRepository
from api.database.recipes.repository import RecipeRepository


class DatabaseRepository(DatabaseConnector):
    items: ItemRepository
    recipes: RecipeRepository
    carts: CartRepository

    def __enter__(self):
        super().__enter__()
        self.items = ItemRepository(self.ctx, self.cursor)
        self.recipes = RecipeRepository(self.ctx, self.cursor)
        self.carts = CartRepository(self.ctx, self.cursor)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self.carts, self.recipes, self.items
        super().__exit__(exc_type, exc_val, exc_tb)

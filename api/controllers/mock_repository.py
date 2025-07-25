from api.controllers.carts.test_repository import CartTestRepository
from api.controllers.faker import Faker
from api.controllers.items.test_repository import ItemTestRepository
from api.controllers.recipes.test_repository import RecipeTestRepository
from api.controllers.test_repository import TestRepository
from api.controllers.users.test_repository import UserTestRepository


class MockRepository(TestRepository):
    def __init__(self):
        super().__init__(None)
        self.faker = Faker()

        self.users = UserTestRepository(self)
        self.items = ItemTestRepository(self)
        self.recipes = RecipeTestRepository(self)
        self.carts = CartTestRepository(self)

        self.users.init_users()
        self.items.init_items()
        self.recipes.init_recipes()
        self.carts.init_carts()

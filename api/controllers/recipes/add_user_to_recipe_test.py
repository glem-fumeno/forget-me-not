import unittest

from api.context import Context
from api.controllers.controllers import Controllers
from api.controllers.mock_repository import MockRepository
from api.faker import Faker
from api.models.recipes.errors import RecipeNotFoundError
from api.models.users.errors import UserNotFoundError


class TestAddUserToRecipe(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = Context()
        self.faker = Faker()
        self.controllers = Controllers(self.ctx, MockRepository())
        self.login = self.faker.login
        self.user = self.controllers.users.register(self.login)
        self.new_login = self.faker.login
        self.new_user = self.controllers.users.register(self.new_login)
        self.ctx.add("token", self.user.token)
        self.recipe = self.controllers.recipes.create(self.faker.recipe)

    def test_raises_error_if_recipe_not_found(self):
        with self.assertRaises(RecipeNotFoundError):
            self.controllers.recipes.add_user_to_recipe(-1, self.user.user_id)

    def test_raises_error_if_user_not_found(self):
        with self.assertRaises(UserNotFoundError):
            self.controllers.recipes.add_user_to_recipe(
                self.recipe.recipe_id, -1
            )

    def test_adds_user_to_recipe(self):
        self.controllers.recipes.add_user_to_recipe(
            self.recipe.recipe_id, self.new_user.user_id
        )
        self.ctx.add("token", self.new_user.token)
        self.controllers.recipes.read(self.recipe.recipe_id)

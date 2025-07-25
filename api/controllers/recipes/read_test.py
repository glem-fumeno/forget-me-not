import unittest

from api.context import Context
from api.controllers.controllers import Controllers
from api.controllers.mock_repository import MockRepository
from api.errors import LoggedOut
from api.models.recipes.errors import RecipeNotFoundError


class TestRead(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = Context()
        self.repository = MockRepository(True)
        self.controllers = Controllers(self.ctx, self.repository)
        self.login = self.repository.faker.login
        self.user = self.controllers.users.register(self.login)
        self.controllers.ctx.add("token", self.user.token)
        self.recipe = self.repository.faker.recipe

    def test_raises_error_if_not_found(self):
        with self.assertRaises(RecipeNotFoundError):
            self.controllers.recipes.read(-1)

    def test_returns_recipe_if_found(self):
        recipe = self.controllers.recipes.create(self.recipe)
        result = self.controllers.recipes.read(recipe.recipe_id)
        self.assertEqual(result.recipe_id, recipe.recipe_id)
        self.assertEqual(result.name, recipe.name)
        self.assertEqual(result.icon, recipe.icon)

    def test_user_logged_out_raises_error(self):
        self.controllers.ctx.add("token", "")
        with self.assertRaises(LoggedOut):
            self.controllers.recipes.read(-1)

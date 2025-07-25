import unittest

from api.context import Context
from api.controllers.controllers import Controllers
from api.controllers.faker import Faker
from api.controllers.mock_repository import MockRepository
from api.errors import LoggedOut
from api.models.recipes.errors import RecipeNotFoundError
from api.models.recipes.requests import RecipeUpdateRequest


class TestUpdate(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = Context()
        self.faker = Faker()
        self.controllers = Controllers(self.ctx, MockRepository())
        self.login = self.faker.login
        self.user = self.controllers.users.register(self.login)
        self.ctx.add("token", self.user.token)
        self.recipe = self.controllers.recipes.create(self.faker.recipe)
        self.request = RecipeUpdateRequest()

    def test_raises_error_if_not_found(self):
        with self.assertRaises(RecipeNotFoundError):
            self.controllers.recipes.update(-1, self.request)

    def test_updates_name(self):
        self.request.name = self.faker.noun
        result = self.controllers.recipes.update(
            self.recipe.recipe_id, self.request
        )
        check = self.controllers.recipes.read(self.recipe.recipe_id)
        self.assertEqual(result, check)

        self.assertEqual(result.recipe_id, self.recipe.recipe_id)
        self.assertEqual(result.name, self.request.name)
        self.assertEqual(result.icon, self.recipe.icon)

    def test_updates_icon(self):
        self.request.icon = self.faker.icon
        result = self.controllers.recipes.update(
            self.recipe.recipe_id, self.request
        )
        check = self.controllers.recipes.read(self.recipe.recipe_id)
        self.assertEqual(result, check)

        self.assertEqual(result.recipe_id, self.recipe.recipe_id)
        self.assertEqual(result.name, self.recipe.name)
        self.assertEqual(result.icon, self.request.icon)

    def test_user_logged_out_raises_error(self):
        self.ctx.add("token", "")
        with self.assertRaises(LoggedOut):
            self.controllers.recipes.update(-1, self.request)

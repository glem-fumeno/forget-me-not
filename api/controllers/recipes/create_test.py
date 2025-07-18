import unittest

from api.context import Context
from api.controllers.mock_repository import MockRepository
from api.controllers.recipes.create import RecipeCreateController
from api.errors import LoggedOut
from api.models.recipes.requests import RecipeCreateRequest


class TestCreate(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = MockRepository()
        user_id = self.repository.email_map["alice.anderson@example.com"]
        self.ctx = Context().add("token", self.repository.login(user_id))
        self.controller = RecipeCreateController(self.ctx, self.repository)

    def test_new_name_creates_recipe(self):
        result = self.controller.run(
            RecipeCreateRequest(
                name="scrambled eggs",
                icon="https://img.icons8.com/pulsar-line/96/sunny-side-up-eggs.png",
            )
        )
        self.assertIn(result.recipe_id, self.repository.recipe_map)

    def test_user_logged_out_raises_error(self):
        self.controller.ctx = self.controller.ctx.add("token", "")
        with self.assertRaises(LoggedOut):
            self.controller.run(
                RecipeCreateRequest(
                    name="scrambled eggs",
                    icon="https://img.icons8.com/pulsar-line/96/sunny-side-up-eggs.png",
                )
            )

import unittest

from api.context import Context
from api.errors import LoggedOut
from api.recipes.controllers.core_test import RecipeTestRepository
from api.recipes.controllers.read import RecipeReadController
from api.recipes.schemas.errors import RecipeNotFoundError


class TestRead(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = RecipeTestRepository()
        self.user_id = self.repository.email_map["alice.anderson@example.com"]
        self.ctx = Context().add("token", self.repository.login(self.user_id))
        self.controller = RecipeReadController(self.ctx, self.repository)

    def test_raises_error_if_not_found(self):
        with self.assertRaises(RecipeNotFoundError):
            self.controller.run(-1)

    def test_returns_recipe_if_found(self):
        user_id = self.repository.email_map["bob.baker@example.com"]
        self.controller.ctx = self.controller.ctx.add(
            "token", self.repository.login(user_id)
        )
        recipe_id = self.repository.recipe_name_map[self.user_id, "pancakes"]
        model = self.repository.recipe_map[recipe_id]
        result = self.controller.run(recipe_id)
        self.assertEqual(result.recipe_id, recipe_id)
        self.assertEqual(result.name, model.name)
        self.assertEqual(result.icon, model.icon)

    def test_user_logged_out_raises_error(self):
        self.controller.ctx = self.controller.ctx.add("token", "")
        with self.assertRaises(LoggedOut):
            self.controller.run(-1)

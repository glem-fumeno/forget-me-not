import unittest

from api.context import Context
from api.errors import LoggedOut
from api.controllers.recipes.core_test import RecipeTestRepository
from api.controllers.recipes.delete import RecipeDeleteController
from api.models.recipes.errors import RecipeNotFoundError


class TestDelete(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = RecipeTestRepository()
        self.user_id = self.repository.email_map["alice.anderson@example.com"]
        self.ctx = Context().add("token", self.repository.login(self.user_id))
        self.controller = RecipeDeleteController(self.ctx, self.repository)

    def test_raises_error_if_not_found(self):
        with self.assertRaises(RecipeNotFoundError):
            self.controller.run(-1)

    def test_found_removes_recipe(self):
        recipe_id = self.repository.recipe_name_map[self.user_id, "omlette"]
        recipe = self.repository.recipe_map[recipe_id]
        result = self.controller.run(recipe_id)
        self.assertNotIn(recipe_id, self.repository.recipe_map)
        self.assertEqual(recipe.recipe_id, result.recipe_id)
        self.assertEqual(recipe.name, result.name)
        self.assertEqual(recipe.icon, result.icon)

    def test_user_logged_out_raises_error(self):
        self.controller.ctx = self.controller.ctx.add("token", "")
        with self.assertRaises(LoggedOut):
            self.controller.run(-1)

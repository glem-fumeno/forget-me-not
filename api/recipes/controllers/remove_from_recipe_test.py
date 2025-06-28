import unittest

from api.context import Context
from api.errors import LoggedOut
from api.recipes.controllers.core_test import RecipeTestRepository
from api.recipes.controllers.remove_from_recipe import (
    RecipeRemoveFromRecipeController,
)
from api.recipes.schemas.errors import ItemNotFoundError, RecipeNotFoundError


class TestRemoveFromRecipe(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = RecipeTestRepository()
        self.user_id = self.repository.email_map["alice.anderson@example.com"]
        self.ctx = Context().add("token", self.repository.login(self.user_id))
        self.controller = RecipeRemoveFromRecipeController(
            self.ctx, self.repository
        )

    def test_raises_error_if_not_found(self):
        with self.assertRaises(RecipeNotFoundError):
            self.controller.run(-1, self.repository.item_name_map["eggs"])

    def test_raises_error_if_item_not_found(self):
        with self.assertRaises(ItemNotFoundError):
            self.controller.run(
                self.repository.recipe_name_map[self.user_id, "pancakes"], -1
            )

    def test_removes_item(self):
        recipe_id = self.repository.recipe_name_map[self.user_id, "pancakes"]
        item_id = self.repository.item_name_map["eggs"]
        result = self.controller.run(recipe_id, item_id)

        assert result.items is not None
        self.assertEqual(len(result.items), 2)

    def test_user_logged_out_raises_error(self):
        self.controller.ctx = self.controller.ctx.add("token", "")
        with self.assertRaises(LoggedOut):
            self.controller.run(-1, -1)

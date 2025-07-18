import unittest

from api.context import Context
from api.controllers.mock_repository import MockRepository
from api.controllers.recipes.add_to_recipe import RecipeAddToRecipeController
from api.errors import LoggedOut
from api.models.items.errors import ItemNotFoundError
from api.models.recipes.errors import RecipeNotFoundError


class TestAddToRecipe(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = MockRepository()
        self.user_id = self.repository.email_map["alice.anderson@example.com"]
        self.ctx = Context().add("token", self.repository.login(self.user_id))
        self.controller = RecipeAddToRecipeController(
            self.ctx, self.repository
        )

    def test_raises_error_if_not_found(self):
        with self.assertRaises(RecipeNotFoundError):
            self.controller.run(-1, self.repository.item_name_map["milk"])

    def test_raises_error_if_item_not_found(self):
        with self.assertRaises(ItemNotFoundError):
            self.controller.run(
                self.repository.recipe_name_map[self.user_id, "omlette"], -1
            )

    def test_upserts_item(self):
        recipe_id = self.repository.recipe_name_map[self.user_id, "omlette"]
        item_id = self.repository.item_name_map["milk"]
        result = self.controller.run(recipe_id, item_id)

        assert result.items is not None
        self.assertEqual(len(result.items), 2)

    def test_user_logged_out_raises_error(self):
        self.controller.ctx = self.controller.ctx.add("token", "")
        with self.assertRaises(LoggedOut):
            self.controller.run(-1, -1)

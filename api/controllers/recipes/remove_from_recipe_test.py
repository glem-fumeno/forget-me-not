import unittest

from api.context import Context
from api.controllers.controllers import Controllers
from api.controllers.mock_repository import MockRepository
from api.errors import LoggedOut
from api.models.items.errors import ItemNotFoundError
from api.models.recipes.errors import RecipeNotFoundError


class TestRemoveFromRecipe(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = Context()
        self.repository = MockRepository(True)
        self.controllers = Controllers(self.ctx, self.repository)
        self.login = self.repository.faker.login
        self.user = self.controllers.users.register(self.login)
        self.controllers.ctx.add("token", self.user.token)
        self.recipe = self.controllers.recipes.create(
            self.repository.faker.recipe
        )
        self.item = self.controllers.items.create(self.repository.faker.item)

    def test_raises_error_if_not_found(self):
        with self.assertRaises(RecipeNotFoundError):
            self.controllers.recipes.remove_from_recipe(-1, self.item.item_id)

    def test_raises_error_if_item_not_found(self):
        with self.assertRaises(ItemNotFoundError):
            self.controllers.recipes.remove_from_recipe(
                self.recipe.recipe_id, -1
            )

    def test_removes_item(self):
        for _ in range(5):
            item = self.controllers.items.create(self.repository.faker.item)
            self.controllers.recipes.add_to_recipe(
                self.recipe.recipe_id, item.item_id
            )
        self.controllers.recipes.add_to_recipe(
            self.recipe.recipe_id, self.item.item_id
        )
        result = self.controllers.recipes.remove_from_recipe(
            self.recipe.recipe_id, self.item.item_id
        )
        check = self.controllers.recipes.read(self.recipe.recipe_id)
        self.assertEqual(result, check)

        assert result.items is not None
        self.assertEqual(len(result.items), 5)

    def test_user_logged_out_raises_error(self):
        self.controllers.ctx.add("token", "")
        with self.assertRaises(LoggedOut):
            self.controllers.recipes.remove_from_recipe(-1, -1)

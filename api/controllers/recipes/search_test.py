import unittest

from api.context import Context
from api.controllers.controllers import Controllers
from api.controllers.mock_repository import MockRepository
from api.errors import LoggedOut
from api.faker import Faker


class TestSearch(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = Context()
        self.faker = Faker()
        self.controllers = Controllers(self.ctx, MockRepository())
        self.login = self.faker.login
        self.user = self.controllers.users.register(self.login)

    def test_returns_all_recipes(self):
        self.ctx.add("token", self.user.token)
        for _ in range(12):
            self.controllers.recipes.create(self.faker.recipe)
        result = self.controllers.recipes.search()
        self.assertEqual(len(result.recipes), 12)
        self.assertEqual(result.count, 12)

    def test_returns_recipes_with_items(self):
        self.ctx.add("token", self.user.token)
        recipe = self.controllers.recipes.create(self.faker.recipe)
        for _ in range(3):
            item = self.controllers.items.create(self.faker.item)
            self.controllers.recipes.add_to_recipe(
                recipe.recipe_id, item.item_id
            )
        result = self.controllers.recipes.search()
        self.assertEqual(len(result.recipes), 1)
        assert result.recipes[0].items is not None
        self.assertEqual(len(result.recipes[0].items), 3)

    def test_user_logged_out_raises_error(self):
        with self.assertRaises(LoggedOut):
            self.controllers.recipes.search()

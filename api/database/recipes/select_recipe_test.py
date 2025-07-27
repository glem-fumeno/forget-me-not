import unittest

from api.context import Context
from api.database.repository import DatabaseRepository
from api.faker import Faker


class TestSelectRecipe(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.faker = Faker()
        self.user = self.faker.user_model
        self.repository.users.insert_user(self.user)
        self.new_user = self.faker.user_model
        self.repository.users.insert_user(self.new_user)
        self.recipe = self.faker.recipe_model

    def test_returns_none_when_no_recipe(self):
        self.repository.recipes.insert_recipe(self.user.user_id, self.recipe)
        result = self.repository.recipes.select_recipe(
            self.new_user.user_id, self.recipe.recipe_id
        )
        self.assertIsNone(result)

    def test_returns_recipe_when_found(self):
        self.repository.recipes.insert_recipe(self.user.user_id, self.recipe)
        result = self.repository.recipes.select_recipe(
            self.user.user_id, self.recipe.recipe_id
        )
        self.assertEqual(result, self.recipe)

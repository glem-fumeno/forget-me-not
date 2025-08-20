import unittest

from api.context import Context
from api.database.repository import DatabaseRepository
from api.faker import Faker


class TestSelectRecipes(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseRepository(Context(), ":memory:")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.faker = Faker()
        self.recipe = self.faker.recipe_model

    def test_returns_all_recipes(self):
        self.repository.recipes.insert_recipe(self.recipe)
        for _ in range(12):
            self.repository.recipes.insert_recipe(self.faker.recipe_model)
        result = self.repository.recipes.select_recipes()
        self.assertEqual(len(result), 13)
        self.assertEqual(result[self.recipe.recipe_id], self.recipe)

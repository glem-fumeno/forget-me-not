import unittest

from api.context import Context
from api.database.repository import DatabaseRepository
from api.faker import Faker


class TestInsertRecipe(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseRepository(Context(), ":memory:")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.faker = Faker()
        self.recipe = self.faker.recipe_model

    def test_changes_recipe_id(self):
        self.repository.recipes.insert_recipe(self.recipe)
        self.assertNotEqual(self.recipe.recipe_id, -1)

    def test_inserts_recipe_to_db(self):
        self.repository.recipes.insert_recipe(self.recipe)
        result = self.repository.recipes.select_recipe(self.recipe.recipe_id)
        self.assertIsNotNone(result)

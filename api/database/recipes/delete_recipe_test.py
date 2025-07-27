import unittest

from api.context import Context
from api.database.repository import DatabaseRepository
from api.faker import Faker


class TestDeleteRecipe(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.faker = Faker()
        self.user = self.faker.user_model
        self.recipe = self.faker.recipe_model

    def test_deletes_recipe_when_found(self):
        self.repository.users.insert_user(self.user)
        self.repository.recipes.insert_recipe(self.user.user_id, self.recipe)
        self.repository.recipes.delete_recipe(self.recipe.recipe_id)
        result = self.repository.recipes.select_recipe(
            self.user.user_id, self.recipe.recipe_id
        )
        self.assertIsNone(result)

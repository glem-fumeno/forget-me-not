import unittest

from api.context import Context
from api.database.repository import DatabaseRepository
from api.faker import Faker


class TestUpdateRecipe(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseRepository(Context(), ":memory:")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.faker = Faker()
        self.user = self.faker.user_model
        self.repository.users.insert_user(self.user)
        self.recipe = self.faker.recipe_model

    def test_updates_recipe_in_db(self):
        self.repository.recipes.insert_recipe(self.user.user_id, self.recipe)
        model = self.faker.recipe_model
        model.recipe_id = self.recipe.recipe_id
        self.repository.recipes.update_recipe(model)
        result = self.repository.recipes.select_recipe(
            self.user.user_id, model.recipe_id
        )
        self.assertEqual(result, model)

import unittest

from api.context import Context
from api.database.repository import DatabaseRepository
from api.faker import Faker


class TestSelectRecipeUsers(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseRepository(Context(), ":memory:")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.faker = Faker()
        self.user = self.faker.user_model
        self.repository.users.insert_user(self.user)
        self.recipe = self.faker.recipe_model

    def test_adds_recipe_to_user_to_db(self):
        self.repository.recipes.insert_recipe(self.user.user_id, self.recipe)
        for _ in range(12):
            user = self.faker.user_model
            self.repository.users.insert_user(user)
            self.repository.recipes.insert_recipe_user(
                self.recipe.recipe_id, user.user_id
            )
        result = self.repository.recipes.select_recipe_users(
            self.recipe.recipe_id
        )
        self.assertEqual(len(result), 13)

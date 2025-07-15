import unittest

from api.context import Context
from api.database.recipes.core_test import RecipeDatabaseTestRepository


class TestSelectRecipe(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = RecipeDatabaseTestRepository(Context(), "test.db")
        self.repository.connect()
        self.repository.initialize_test_cases()

    def tearDown(self) -> None:
        self.repository.connection.rollback()
        self.repository.connection.close()

    def test_returns_none_when_no_recipe(self):
        user_id = self.repository.email_map["bob.baker@example.com"]
        owner_id = self.repository.email_map["alice.anderson@example.com"]
        recipe_id = self.repository.recipe_name_map[owner_id, "omlette"]
        result = self.repository.select_recipe(user_id, recipe_id)
        self.assertIsNone(result)

    def test_returns_recipe_when_found(self):
        user_id = self.repository.email_map["alice.anderson@example.com"]
        recipe_id = self.repository.recipe_name_map[user_id, "omlette"]
        result = self.repository.select_recipe(user_id, recipe_id)
        self.assertEqual(result, self.repository.recipe_map[recipe_id])

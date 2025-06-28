import unittest

from api.context import Context
from api.recipes.database.core_test import RecipeDatabaseTestRepository


class TestSelectRecipes(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = RecipeDatabaseTestRepository(Context(), "test.db")
        self.repository.connect()
        self.repository.initialize_test_cases()

    def tearDown(self) -> None:
        self.repository.connection.rollback()
        self.repository.connection.close()

    def test_returns_all_recipes(self):
        user_id = self.repository.email_map["alice.anderson@example.com"]
        result = self.repository.select_recipes(user_id)
        self.assertEqual(len(result), 2)
        self.assertIn(
            self.repository.recipe_name_map[user_id, "omlette"], result
        )
        self.assertIn(
            self.repository.recipe_name_map[user_id, "pancakes"], result
        )

import unittest

from api.context import Context
from api.database.test_repository import DatabaseTestRepository


class TestSelectRecipes(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseTestRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.repository.initialize_test_cases()

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

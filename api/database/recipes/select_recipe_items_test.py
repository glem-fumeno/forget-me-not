import unittest

from api.context import Context
from api.database.test_repository import DatabaseTestRepository


class TestSelectRecipeItems(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseTestRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.repository.initialize_test_cases()

    def test_returns_all_recipe_items(self):
        user_id = self.repository.email_map["alice.anderson@example.com"]
        recipe_id = self.repository.recipe_name_map[user_id, "pancakes"]
        result = self.repository.select_recipe_items(recipe_id)
        self.assertEqual(len(result), 3)
        self.assertIn(self.repository.item_name_map["eggs"], result)
        self.assertIn(self.repository.item_name_map["flour"], result)
        self.assertIn(self.repository.item_name_map["milk"], result)

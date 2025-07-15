import unittest

from api.context import Context
from api.database.recipes.core_test import RecipeDatabaseTestRepository


class TestSelectRecipeItems(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = RecipeDatabaseTestRepository(Context(), "test.db")
        self.repository.connect()
        self.repository.initialize_test_cases()

    def tearDown(self) -> None:
        self.repository.connection.rollback()
        self.repository.connection.close()

    def test_returns_all_recipe_items(self):
        user_id = self.repository.email_map["alice.anderson@example.com"]
        recipe_id = self.repository.recipe_name_map[user_id, "pancakes"]
        result = self.repository.select_recipe_items(recipe_id)
        self.assertEqual(len(result), 3)
        self.assertEqual(
            self.repository.item_map[self.repository.item_name_map["eggs"]],
            result[0],
        )
        self.assertEqual(
            self.repository.item_map[self.repository.item_name_map["flour"]],
            result[1],
        )
        self.assertEqual(
            self.repository.item_map[self.repository.item_name_map["milk"]],
            result[2],
        )

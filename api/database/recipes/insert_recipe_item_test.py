import unittest

from api.context import Context
from api.database.test_repository import DatabaseTestRepository


class TestInsertRecipeItem(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseTestRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.repository.initialize_test_cases()

    def test_inserts_recipe_item_to_db(self):
        user_id = self.repository.email_map["alice.anderson@example.com"]
        recipe_id = self.repository.recipe_name_map[user_id, "omlette"]
        item_id = self.repository.item_name_map["milk"]
        self.repository.recipes.insert_recipe_item(recipe_id, item_id)
        result = self.repository.cursor.execute(
            """
            SELECT recipe_id_
            FROM recipes_items_
            WHERE recipe_id_ = ? AND item_id_ = ?
            """,
            (recipe_id, item_id),
        )
        self.assertEqual(recipe_id, result.fetchone()[0])

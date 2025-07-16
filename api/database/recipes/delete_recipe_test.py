import unittest

from api.context import Context
from api.database.test_repository import DatabaseTestRepository


class TestDeleteRecipe(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseTestRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.repository.initialize_test_cases()

    def test_returns_recipe_when_found(self):
        user_id = self.repository.email_map["alice.anderson@example.com"]
        recipe_id = self.repository.recipe_name_map[user_id, "pancakes"]
        self.repository.delete_recipe(recipe_id)
        result = self.repository.cursor.execute(
            """
            SELECT recipe_id_ FROM recipes_ WHERE recipe_id_ = ?
            """,
            (recipe_id,),
        )
        self.assertIsNone(result.fetchone())

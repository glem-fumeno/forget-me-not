import unittest

from api.context import Context
from api.database.recipes.core_test import RecipeDatabaseTestRepository


class TestDeleteRecipe(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = RecipeDatabaseTestRepository(Context(), "test.db")
        self.repository.connect()
        self.repository.initialize_test_cases()

    def tearDown(self) -> None:
        self.repository.connection.rollback()
        self.repository.connection.close()

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

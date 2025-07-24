import unittest

from api.context import Context
from api.database.test_repository import DatabaseTestRepository
from api.models.recipes.models import RecipeModel


class TestInsertRecipe(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseTestRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.repository.initialize_test_cases()

    def test_changes_recipe_id(self):
        model = RecipeModel(
            recipe_id=-1,
            name="scrambled eggs",
            icon="https://img.icons8.com/pulsar-line/96/sunny-side-up-eggs.png",
        )
        user_id = self.repository.email_map["alice.anderson@example.com"]
        self.repository.recipes.insert_recipe(user_id, model)
        self.assertNotEqual(model.recipe_id, -1)

    def test_inserts_recipe_to_db(self):
        model = RecipeModel(
            recipe_id=-1,
            name="scrambled eggs",
            icon="https://img.icons8.com/pulsar-line/96/sunny-side-up-eggs.png",
        )
        user_id = self.repository.email_map["alice.anderson@example.com"]
        self.repository.recipes.insert_recipe(user_id, model)
        result = self.repository.cursor.execute(
            """
            SELECT recipe_id_ FROM recipes_ WHERE recipe_id_ = ?
            """,
            (model.recipe_id,),
        )
        self.assertEqual(model.recipe_id, result.fetchone()[0])

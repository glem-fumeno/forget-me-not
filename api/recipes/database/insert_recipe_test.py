import unittest

from api.context import Context
from api.recipes.database.core_test import RecipeDatabaseTestRepository
from api.recipes.schemas.models import RecipeModel


class TestInsertRecipe(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = RecipeDatabaseTestRepository(Context(), "test.db")
        self.repository.connect()
        self.repository.initialize_test_cases()

    def tearDown(self) -> None:
        self.repository.connection.rollback()
        self.repository.connection.close()

    def test_changes_recipe_id(self):
        model = RecipeModel(
            recipe_id=-1,
            name="scrambled eggs",
            icon="https://img.icons8.com/pulsar-line/96/sunny-side-up-eggs.png",
        )
        user_id = self.repository.email_map["alice.anderson@example.com"]
        self.repository.insert_recipe(user_id, model)
        self.assertNotEqual(model.recipe_id, -1)

    def test_inserts_recipe_to_db(self):
        model = RecipeModel(
            recipe_id=-1,
            name="scrambled eggs",
            icon="https://img.icons8.com/pulsar-line/96/sunny-side-up-eggs.png",
        )
        user_id = self.repository.email_map["alice.anderson@example.com"]
        self.repository.insert_recipe(user_id, model)
        result = self.repository.cursor.execute(
            """
            SELECT recipe_id_ FROM recipes_ WHERE recipe_id_ = ?
            """,
            (model.recipe_id,),
        )
        self.assertEqual(model.recipe_id, result.fetchone()[0])

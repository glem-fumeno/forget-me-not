import unittest

from api.context import Context
from api.database.test_repository import DatabaseTestRepository
from api.models.recipes.models import RecipeModel


class TestUpdateRecipe(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseTestRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.repository.initialize_test_cases()

    def test_updates_recipe_in_db(self):
        user_id = self.repository.email_map["alice.anderson@example.com"]
        recipe_id = self.repository.recipe_name_map[user_id, "omlette"]
        model = RecipeModel(
            recipe_id=recipe_id,
            name="scrambled eggs",
            icon="https://img.icons8.com/pulsar-line/96/sunny-side-up-eggs.png",
        )
        self.repository.update_recipe(model)
        result = self.repository.cursor.execute(
            """
            SELECT recipe_id_, name_, icon_ FROM recipes_ WHERE recipe_id_ = ?
            """,
            (recipe_id,),
        )
        new_model = RecipeModel.from_db(result.description, result.fetchone())
        self.assertEqual(model, new_model)

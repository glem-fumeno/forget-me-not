import unittest

from api.context import Context
from api.recipes.database.core_test import RecipeDatabaseTestRepository
from api.recipes.schemas.models import RecipeUserModel


class TestInsertRecipeUser(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = RecipeDatabaseTestRepository(Context(), "test.db")
        self.repository.connect()
        self.repository.initialize_test_cases()

    def tearDown(self) -> None:
        self.repository.connection.rollback()
        self.repository.connection.close()

    def test_inserts_recipe_session_to_db(self):
        owner_id = self.repository.email_map["alice.anderson@example.com"]
        user_id = self.repository.email_map["bob.baker@example.com"]
        recipe_id = self.repository.recipe_name_map[owner_id, "omlette"]
        model = RecipeUserModel(recipe_id=recipe_id, user_id=user_id)
        self.repository.insert_recipe_user(model)
        result = self.repository.cursor.execute(
            """
            SELECT recipe_id_
            FROM recipes_users_
            WHERE user_id_ = ? AND recipe_id_ = ?
            """,
            (model.user_id, model.recipe_id),
        )
        self.assertEqual(model.recipe_id, result.fetchone()[0])

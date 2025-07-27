import unittest

from api.context import Context
from api.database.repository import DatabaseRepository
from api.faker import Faker


class TestDeleteRecipeItem(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.faker = Faker()
        self.item = self.faker.item_model
        self.user = self.faker.user_model
        self.recipe = self.faker.recipe_model

    def test_deletes_recipe_item_from_db(self):
        self.repository.users.insert_user(self.user)
        self.repository.recipes.insert_recipe(self.user.user_id, self.recipe)
        self.repository.items.insert_item(self.item)
        self.repository.recipes.insert_recipe_item(
            self.recipe.recipe_id, self.item.item_id
        )
        for _ in range(5):
            item = self.faker.item_model
            self.repository.items.insert_item(item)
            self.repository.recipes.insert_recipe_item(
                self.recipe.recipe_id, item.item_id
            )
        self.repository.recipes.delete_recipe_item(
            self.recipe.recipe_id, self.item.item_id
        )
        result = self.repository.recipes.select_recipe_items(
            self.recipe.recipe_id
        )
        self.assertEqual(len(result), 5)
        self.assertNotIn(self.item.item_id, result)

from api.models.recipes.errors import RecipeNotFoundError
from api.test_case import TestCase


class TestDelete(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.recipe = self.faker.recipe

    def test_raises_error_if_not_found(self):
        with self.assertRaises(RecipeNotFoundError):
            self.controllers.recipes.delete(-1)

    def test_found_removes_recipe(self):
        recipe = self.controllers.recipes.create(self.recipe)
        result = self.controllers.recipes.delete(recipe.recipe_id)
        self.assertEqual(recipe.recipe_id, result.recipe_id)
        self.assertEqual(recipe.name, result.name)
        self.assertEqual(recipe.icon, result.icon)
        with self.assertRaises(RecipeNotFoundError):
            self.controllers.recipes.read(recipe.recipe_id)

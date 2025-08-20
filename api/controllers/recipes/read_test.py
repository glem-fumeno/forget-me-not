from api.models.recipes.errors import RecipeNotFoundError
from api.test_case import TestCase


class TestRead(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.recipe = self.faker.recipe

    def test_raises_error_if_not_found(self):
        with self.assertRaises(RecipeNotFoundError):
            self.controllers.recipes.read(-1)

    def test_returns_recipe_if_found(self):
        recipe = self.controllers.recipes.create(self.recipe)
        result = self.controllers.recipes.read(recipe.recipe_id)
        self.assertEqual(result.recipe_id, recipe.recipe_id)
        self.assertEqual(result.name, recipe.name)
        self.assertEqual(result.icon, recipe.icon)

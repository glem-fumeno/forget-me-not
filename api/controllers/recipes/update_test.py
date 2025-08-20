from api.models.recipes.errors import RecipeNotFoundError
from api.models.recipes.requests import RecipeUpdateRequest
from api.test_case import TestCase


class TestUpdate(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.recipe = self.controllers.recipes.create(self.faker.recipe)
        self.request = RecipeUpdateRequest()

    def test_raises_error_if_not_found(self):
        with self.assertRaises(RecipeNotFoundError):
            self.controllers.recipes.update(-1, self.request)

    def test_updates_name(self):
        self.request.name = self.faker.noun
        result = self.controllers.recipes.update(
            self.recipe.recipe_id, self.request
        )
        check = self.controllers.recipes.read(self.recipe.recipe_id)
        self.assertEqual(result, check)

        self.assertEqual(result.recipe_id, self.recipe.recipe_id)
        self.assertEqual(result.name, self.request.name)
        self.assertEqual(result.icon, self.recipe.icon)

    def test_updates_icon(self):
        self.request.icon = self.faker.icon
        result = self.controllers.recipes.update(
            self.recipe.recipe_id, self.request
        )
        check = self.controllers.recipes.read(self.recipe.recipe_id)
        self.assertEqual(result, check)

        self.assertEqual(result.recipe_id, self.recipe.recipe_id)
        self.assertEqual(result.name, self.recipe.name)
        self.assertEqual(result.icon, self.request.icon)

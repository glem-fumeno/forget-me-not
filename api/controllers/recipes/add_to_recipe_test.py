from api.models.items.errors import ItemNotFoundError
from api.models.recipes.errors import RecipeNotFoundError
from api.test_case import TestCase


class TestAddToRecipe(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.recipe = self.controllers.recipes.create(self.faker.recipe)
        self.item = self.controllers.items.create(self.faker.item)

    def test_raises_error_if_not_found(self):
        with self.assertRaises(RecipeNotFoundError):
            self.controllers.recipes.add_to_recipe(-1, self.item.item_id)

    def test_raises_error_if_item_not_found(self):
        with self.assertRaises(ItemNotFoundError):
            self.controllers.recipes.add_to_recipe(self.recipe.recipe_id, -1)

    def test_upserts_item(self):
        for _ in range(5):
            item = self.controllers.items.create(self.faker.item)
            self.controllers.recipes.add_to_recipe(
                self.recipe.recipe_id, item.item_id
            )
        result = self.controllers.recipes.add_to_recipe(
            self.recipe.recipe_id, self.item.item_id
        )
        check = self.controllers.recipes.read(self.recipe.recipe_id)
        self.assertEqual(result, check)

        assert result.items is not None
        self.assertEqual(len(result.items), 6)

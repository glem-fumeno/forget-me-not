from api.test_case import TestCase


class TestSearch(TestCase):

    def test_returns_all_recipes(self):
        for _ in range(12):
            self.controllers.recipes.create(self.faker.recipe)
        result = self.controllers.recipes.search()
        self.assertEqual(len(result.recipes), 12)
        self.assertEqual(result.count, 12)

    def test_returns_recipes_with_items(self):
        recipe = self.controllers.recipes.create(self.faker.recipe)
        for _ in range(3):
            item = self.controllers.items.create(self.faker.item)
            self.controllers.recipes.add_to_recipe(
                recipe.recipe_id, item.item_id
            )
        result = self.controllers.recipes.search()
        self.assertEqual(len(result.recipes), 1)
        assert result.recipes[0].items is not None
        self.assertEqual(len(result.recipes[0].items), 3)

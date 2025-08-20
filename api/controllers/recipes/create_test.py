from api.test_case import TestCase


class TestCreate(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.request = self.faker.recipe

    def test_new_name_creates_recipe(self):
        result = self.controllers.recipes.create(self.request)
        check = self.controllers.recipes.read(result.recipe_id)
        self.assertEqual(result, check)

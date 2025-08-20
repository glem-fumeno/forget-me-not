from api.models.carts.errors import CartNotFoundError
from api.models.recipes.errors import RecipeNotFoundError
from api.test_case import TestCase


class TestAddRecipeToCart(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.cart = self.controllers.carts.create(self.faker.cart)
        self.recipe = self.controllers.recipes.create(self.faker.recipe)
        self.item = self.controllers.items.create(self.faker.item)

    def test_raises_error_if_not_found(self):
        with self.assertRaises(CartNotFoundError):
            self.controllers.carts.add_recipe_to_cart(
                -1, self.recipe.recipe_id
            )

    def test_raises_error_if_recipe_not_found(self):
        with self.assertRaises(RecipeNotFoundError):
            self.controllers.carts.add_recipe_to_cart(self.cart.cart_id, -1)

    def test_upserts_items(self):
        self.controllers.recipes.add_to_recipe(
            self.recipe.recipe_id, self.item.item_id
        )
        for _ in range(5):
            item = self.controllers.items.create(self.faker.item)
            self.controllers.recipes.add_to_recipe(
                self.recipe.recipe_id, item.item_id
            )
        self.controllers.carts.add_to_cart(
            self.cart.cart_id, self.item.item_id
        )
        for _ in range(3):
            item = self.controllers.items.create(self.faker.item)
            self.controllers.carts.add_to_cart(self.cart.cart_id, item.item_id)
        result = self.controllers.carts.add_recipe_to_cart(
            self.cart.cart_id, self.recipe.recipe_id
        )
        check = self.controllers.carts.read(self.cart.cart_id)
        self.assertEqual(result, check)

        assert result.items is not None
        self.assertEqual(len(result.items), 10)

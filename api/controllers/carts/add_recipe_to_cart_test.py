import unittest

from api.context import Context
from api.controllers.controllers import Controllers
from api.controllers.mock_repository import MockRepository
from api.errors import LoggedOut
from api.models.carts.errors import CartNotFoundError
from api.models.recipes.errors import RecipeNotFoundError


class TestAddRecipeToCart(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = MockRepository()
        self.user_id = self.repository.email_map["alice.anderson@example.com"]
        self.ctx = Context().add("token", self.repository.login(self.user_id))
        self.controllers = Controllers(self.ctx, self.repository)

    def test_raises_error_if_not_found(self):
        with self.assertRaises(CartNotFoundError):
            self.controllers.carts.add_recipe_to_cart(
                -1, self.repository.recipe_name_map[self.user_id, "pancakes"]
            )

    def test_raises_error_if_recipe_not_found(self):
        with self.assertRaises(RecipeNotFoundError):
            self.controllers.carts.add_recipe_to_cart(
                self.repository.cart_name_map[self.user_id, "groceries"], -1
            )

    def test_upserts_items(self):
        cart_id = self.repository.cart_name_map[self.user_id, "groceries"]
        recipe_id = self.repository.recipe_name_map[self.user_id, "pancakes"]
        result = self.controllers.carts.add_recipe_to_cart(cart_id, recipe_id)

        assert result.items is not None
        self.assertEqual(len(result.items), 4)

    def test_user_logged_out_raises_error(self):
        self.controllers.carts.ctx = self.controllers.carts.ctx.add("token", "")
        with self.assertRaises(LoggedOut):
            self.controllers.carts.add_recipe_to_cart(-1, -1)

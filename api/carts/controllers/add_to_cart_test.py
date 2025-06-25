import unittest

from api.carts.controllers.add_to_cart import CartAddToCartController
from api.carts.controllers.core_test import CartTestRepository
from api.carts.schemas.errors import CartNotFoundError, ItemNotFoundError
from api.context import Context
from api.errors import LoggedOut


class TestAddToCart(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = CartTestRepository()
        self.user_id = self.repository.email_map["alice.anderson@example.com"]
        self.ctx = Context().add("token", self.repository.login(self.user_id))
        self.controller = CartAddToCartController(self.ctx, self.repository)

    def test_raises_error_if_not_found(self):
        with self.assertRaises(CartNotFoundError):
            self.controller.run(-1, self.repository.item_name_map["soap"])

    def test_raises_error_if_item_not_found(self):
        with self.assertRaises(ItemNotFoundError):
            self.controller.run(
                self.repository.cart_name_map[self.user_id, "groceries"], -1
            )

    def test_upserts_item(self):
        cart_id = self.repository.cart_name_map[self.user_id, "groceries"]
        item_id = self.repository.item_name_map["soap"]
        result = self.controller.run(cart_id, item_id)

        assert result.items is not None
        self.assertEqual(len(result.items), 3)

    def test_user_logged_out_raises_error(self):
        self.controller.ctx = self.controller.ctx.add("token", "")
        with self.assertRaises(LoggedOut):
            self.controller.run(-1, -1)

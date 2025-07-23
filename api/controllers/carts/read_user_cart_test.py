import unittest

from api.context import Context
from api.controllers.carts.read_user_cart import CartReadUserCartController
from api.controllers.mock_repository import MockRepository
from api.errors import LoggedOut
from api.models.carts.errors import CartNotFoundError


class TestReadUserCart(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = MockRepository()
        self.user_id = self.repository.email_map["alice.anderson@example.com"]
        self.ctx = Context().add("token", self.repository.login(self.user_id))
        self.controller = CartReadUserCartController(self.ctx, self.repository)

    def test_raises_error_if_not_found(self):
        with self.assertRaises(CartNotFoundError):
            self.controller.run()

    def test_raises_error_if_no_longer_found(self):
        self.repository.user_default_cart_map[self.user_id] = -1
        with self.assertRaises(CartNotFoundError):
            self.controller.run()

    def test_returns_cart_if_found(self):
        cart_id = self.repository.cart_name_map[self.user_id, "groceries"]
        self.repository.user_default_cart_map[self.user_id] = cart_id
        result = self.controller.run()
        self.assertEqual(result.cart_id, cart_id)

    def test_user_logged_out_raises_error(self):
        self.controller.ctx = self.controller.ctx.add("token", "")
        with self.assertRaises(LoggedOut):
            self.controller.run()

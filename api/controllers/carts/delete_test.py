import unittest

from api.context import Context
from api.controllers.carts.delete import CartDeleteController
from api.controllers.mock_repository import MockRepository
from api.errors import LoggedOut
from api.models.carts.errors import CartNotFoundError


class TestDelete(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = MockRepository()
        self.user_id = self.repository.email_map["alice.anderson@example.com"]
        self.ctx = Context().add("token", self.repository.login(self.user_id))
        self.controller = CartDeleteController(self.ctx, self.repository)

    def test_raises_error_if_not_found(self):
        with self.assertRaises(CartNotFoundError):
            self.controller.run(-1)

    def test_found_removes_cart(self):
        cart_id = self.repository.cart_name_map[self.user_id, "groceries"]
        cart = self.repository.cart_map[cart_id]
        result = self.controller.run(cart_id)
        self.assertNotIn(cart_id, self.repository.cart_map)
        self.assertEqual(cart.cart_id, result.cart_id)
        self.assertEqual(cart.name, result.name)
        self.assertEqual(cart.icon, result.icon)

    def test_user_logged_out_raises_error(self):
        self.controller.ctx = self.controller.ctx.add("token", "")
        with self.assertRaises(LoggedOut):
            self.controller.run(-1)

import unittest

from api.context import Context
from api.controllers.carts.set_user_cart import CartSetUserCartController
from api.controllers.mock_repository import MockRepository
from api.errors import LoggedOut
from api.models.carts.errors import CartNotFoundError


class TestSetUserCart(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = MockRepository()
        self.user_id = self.repository.email_map["alice.anderson@example.com"]
        self.ctx = Context().add("token", self.repository.login(self.user_id))
        self.controller = CartSetUserCartController(self.ctx, self.repository)

    def test_raises_error_if_not_found(self):
        with self.assertRaises(CartNotFoundError):
            self.controller.run(-1)

    def test_sets_user_cart(self):
        cart_id = self.repository.cart_name_map[self.user_id, "groceries"]
        self.controller.run(cart_id)
        self.assertIn(self.user_id, self.repository.user_default_cart_map)
        self.assertEqual(
            cart_id, self.repository.user_default_cart_map[self.user_id]
        )

    def test_user_logged_out_raises_error(self):
        self.controller.ctx = self.controller.ctx.add("token", "")
        with self.assertRaises(LoggedOut):
            self.controller.run(-1)

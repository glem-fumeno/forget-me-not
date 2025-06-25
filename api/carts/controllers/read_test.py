import unittest

from api.carts.controllers.core_test import CartTestRepository
from api.carts.controllers.read import CartReadController
from api.carts.schemas.errors import CartNotFoundError
from api.context import Context
from api.errors import LoggedOut


class TestRead(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = CartTestRepository()
        self.user_id = self.repository.email_map["alice.anderson@example.com"]
        self.ctx = Context().add("token", self.repository.login(self.user_id))
        self.controller = CartReadController(self.ctx, self.repository)

    def test_raises_error_if_not_found(self):
        with self.assertRaises(CartNotFoundError):
            self.controller.run(-1)

    def test_returns_cart_if_found(self):
        user_id = self.repository.email_map["bob.baker@example.com"]
        self.controller.ctx = self.controller.ctx.add(
            "token", self.repository.login(user_id)
        )
        cart_id = self.repository.cart_name_map[self.user_id, "groceries"]
        model = self.repository.cart_map[cart_id]
        result = self.controller.run(cart_id)
        self.assertEqual(result.cart_id, cart_id)
        self.assertEqual(result.name, model.name)
        self.assertEqual(result.icon, model.icon)

    def test_user_logged_out_raises_error(self):
        self.controller.ctx = self.controller.ctx.add("token", "")
        with self.assertRaises(LoggedOut):
            self.controller.run(-1)

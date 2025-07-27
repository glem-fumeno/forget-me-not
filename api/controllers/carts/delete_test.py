import unittest

from api.context import Context
from api.controllers.controllers import Controllers
from api.controllers.mock_repository import MockRepository
from api.errors import LoggedOut
from api.faker import Faker
from api.models.carts.errors import CartNotFoundError


class TestDelete(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = Context()
        self.faker = Faker()
        self.controllers = Controllers(self.ctx, MockRepository())
        self.login = self.faker.login
        self.user = self.controllers.users.register(self.login)
        self.ctx.add("token", self.user.token)
        self.cart = self.faker.cart

    def test_raises_error_if_not_found(self):
        with self.assertRaises(CartNotFoundError):
            self.controllers.carts.delete(-1)

    def test_found_removes_cart(self):
        cart = self.controllers.carts.create(self.cart)
        result = self.controllers.carts.delete(cart.cart_id)
        self.assertEqual(cart.cart_id, result.cart_id)
        self.assertEqual(cart.name, result.name)
        self.assertEqual(cart.icon, result.icon)
        with self.assertRaises(CartNotFoundError):
            self.controllers.carts.read(cart.cart_id)

    def test_user_logged_out_raises_error(self):
        self.ctx.add("token", "")
        with self.assertRaises(LoggedOut):
            self.controllers.carts.delete(-1)

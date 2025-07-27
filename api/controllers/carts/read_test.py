import unittest

from api.context import Context
from api.controllers.controllers import Controllers
from api.controllers.mock_repository import MockRepository
from api.errors import LoggedOut
from api.faker import Faker
from api.models.carts.errors import CartNotFoundError


class TestRead(unittest.TestCase):
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
            self.controllers.carts.read(-1)

    def test_returns_cart_if_found(self):
        cart = self.controllers.carts.create(self.cart)
        result = self.controllers.carts.read(cart.cart_id)
        self.assertEqual(result.cart_id, cart.cart_id)
        self.assertEqual(result.name, cart.name)
        self.assertEqual(result.icon, cart.icon)

    def test_user_logged_out_raises_error(self):
        self.ctx.add("token", "")
        with self.assertRaises(LoggedOut):
            self.controllers.carts.read(-1)

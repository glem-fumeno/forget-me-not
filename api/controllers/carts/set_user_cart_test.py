import unittest

from api.context import Context
from api.controllers.controllers import Controllers
from api.controllers.faker import Faker
from api.controllers.mock_repository import MockRepository
from api.errors import LoggedOut
from api.models.carts.errors import CartNotFoundError


class TestSetUserCart(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = Context()
        self.faker = Faker()
        self.controllers = Controllers(self.ctx, MockRepository())
        self.login = self.faker.login
        self.user = self.controllers.users.register(self.login)
        self.ctx.add("token", self.user.token)
        self.cart = self.controllers.carts.create(self.faker.cart)

    def test_raises_error_if_not_found(self):
        with self.assertRaises(CartNotFoundError):
            self.controllers.carts.set_user_cart(-1)

    def test_sets_user_cart(self):
        result = self.controllers.carts.set_user_cart(self.cart.cart_id)
        check = self.controllers.carts.read(self.cart.cart_id)
        self.assertEqual(check, result)

    def test_user_logged_out_raises_error(self):
        self.ctx.add("token", "")
        with self.assertRaises(LoggedOut):
            self.controllers.carts.set_user_cart(-1)

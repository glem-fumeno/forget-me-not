import unittest

from api.context import Context
from api.controllers.controllers import Controllers
from api.controllers.faker import Faker
from api.controllers.mock_repository import MockRepository
from api.errors import LoggedOut
from api.models.carts.errors import CartNotFoundError


class TestReadUserCart(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = Context()
        self.faker = Faker()
        self.controllers = Controllers(self.ctx, MockRepository())
        self.login = self.faker.login
        self.user = self.controllers.users.register(self.login)
        self.ctx.add("token", self.user.token)
        self.cart = self.controllers.carts.create(self.faker.cart)
        self.new_cart = self.controllers.carts.create(self.faker.cart)

    def test_raises_error_if_not_found(self):
        with self.assertRaises(CartNotFoundError):
            self.controllers.carts.read_user_cart()

    def test_raises_error_if_no_longer_found(self):
        self.controllers.carts.set_user_cart(self.cart.cart_id)
        self.controllers.carts.delete(self.cart.cart_id)
        with self.assertRaises(CartNotFoundError):
            self.controllers.carts.read_user_cart()

    def test_returns_cart_if_found(self):
        self.controllers.carts.set_user_cart(self.new_cart.cart_id)
        check = self.controllers.carts.read(self.new_cart.cart_id)
        result = self.controllers.carts.read_user_cart()
        self.assertEqual(check, result)

    def test_user_logged_out_raises_error(self):
        self.ctx.add("token", "")
        with self.assertRaises(LoggedOut):
            self.controllers.carts.read_user_cart()

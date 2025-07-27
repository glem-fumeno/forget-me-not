import unittest

from api.context import Context
from api.controllers.controllers import Controllers
from api.controllers.mock_repository import MockRepository
from api.faker import Faker
from api.models.carts.errors import CartNotFoundError
from api.models.users.errors import UserNotFoundError


class TestAddUserToCart(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = Context()
        self.faker = Faker()
        self.controllers = Controllers(self.ctx, MockRepository())
        self.login = self.faker.login
        self.user = self.controllers.users.register(self.login)
        self.new_login = self.faker.login
        self.new_user = self.controllers.users.register(self.new_login)
        self.ctx.add("token", self.user.token)
        self.cart = self.controllers.carts.create(self.faker.cart)

    def test_raises_error_if_cart_not_found(self):
        with self.assertRaises(CartNotFoundError):
            self.controllers.carts.add_user_to_cart(-1, self.user.user_id)

    def test_raises_error_if_user_not_found(self):
        with self.assertRaises(UserNotFoundError):
            self.controllers.carts.add_user_to_cart(self.cart.cart_id, -1)

    def test_adds_user_to_cart(self):
        self.controllers.carts.add_user_to_cart(
            self.cart.cart_id, self.new_user.user_id
        )
        self.ctx.add("token", self.new_user.token)
        self.controllers.carts.read(self.cart.cart_id)

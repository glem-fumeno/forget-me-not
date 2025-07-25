import unittest

from api.context import Context
from api.controllers.controllers import Controllers
from api.controllers.faker import Faker
from api.controllers.mock_repository import MockRepository
from api.errors import LoggedOut
from api.models.carts.errors import CartNotFoundError
from api.models.carts.requests import CartUpdateRequest


class TestUpdate(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = Context()
        self.faker = Faker()
        self.controllers = Controllers(self.ctx, MockRepository())
        self.login = self.faker.login
        self.user = self.controllers.users.register(self.login)
        self.ctx.add("token", self.user.token)
        self.cart = self.controllers.carts.create(self.faker.cart)
        self.request = CartUpdateRequest()

    def test_raises_error_if_not_found(self):
        with self.assertRaises(CartNotFoundError):
            self.controllers.carts.update(-1, self.request)

    def test_updates_name(self):
        self.request.name = self.faker.noun
        result = self.controllers.carts.update(self.cart.cart_id, self.request)
        check = self.controllers.carts.read(self.cart.cart_id)
        self.assertEqual(result, check)

        self.assertEqual(result.cart_id, self.cart.cart_id)
        self.assertEqual(result.name, self.request.name)
        self.assertEqual(result.icon, self.cart.icon)

    def test_updates_icon(self):
        self.request.icon = self.faker.icon
        result = self.controllers.carts.update(self.cart.cart_id, self.request)
        check = self.controllers.carts.read(self.cart.cart_id)
        self.assertEqual(result, check)

        self.assertEqual(result.cart_id, self.cart.cart_id)
        self.assertEqual(result.name, self.cart.name)
        self.assertEqual(result.icon, self.request.icon)

    def test_user_logged_out_raises_error(self):
        self.ctx.add("token", "")
        with self.assertRaises(LoggedOut):
            self.controllers.carts.update(-1, self.request)

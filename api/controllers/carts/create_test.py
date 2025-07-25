import unittest

from api.context import Context
from api.controllers.controllers import Controllers
from api.controllers.faker import Faker
from api.controllers.mock_repository import MockRepository
from api.errors import LoggedOut


class TestCreate(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = Context()
        self.faker = Faker()
        self.controllers = Controllers(self.ctx, MockRepository())
        self.login = self.faker.login
        self.user = self.controllers.users.register(self.login)
        self.request = self.faker.cart

    def test_new_name_creates_cart(self):
        self.ctx.add("token", self.user.token)
        result = self.controllers.carts.create(self.request)
        check = self.controllers.carts.read(result.cart_id)
        self.assertEqual(result, check)

    def test_user_logged_out_raises_error(self):
        with self.assertRaises(LoggedOut):
            self.controllers.carts.create(self.request)

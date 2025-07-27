import unittest

from api.context import Context
from api.controllers.controllers import Controllers
from api.controllers.mock_repository import MockRepository
from api.errors import Inaccessible, LoggedOut
from api.faker import Faker
from api.models.items.errors import ItemNotFoundError


class TestDelete(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = Context()
        self.faker = Faker()
        self.controllers = Controllers(self.ctx, MockRepository())
        self.login = self.faker.login
        self.user = self.controllers.users.register(self.login)
        self.item = self.faker.item

    def test_raises_error_if_not_found(self):
        self.ctx.add("token", self.user.token)
        with self.assertRaises(ItemNotFoundError):
            self.controllers.items.delete(-1)

    def test_found_removes_item(self):
        self.ctx.add("token", self.user.token)
        item = self.controllers.items.create(self.item)
        result = self.controllers.items.delete(item.item_id)
        self.assertEqual(item, result)
        with self.assertRaises(ItemNotFoundError):
            self.controllers.items.read(item.item_id)

    def test_user_logged_out_raises_error(self):
        with self.assertRaises(LoggedOut):
            self.controllers.items.delete(-1)

    def test_user_role_raises_error(self):
        user = self.controllers.users.register(self.faker.login)
        self.ctx.add("token", user.token)
        with self.assertRaises(Inaccessible):
            self.controllers.items.delete(-1)

import unittest

from api.context import Context
from api.controllers.controllers import Controllers
from api.controllers.mock_repository import MockRepository
from api.errors import LoggedOut
from api.models.items.errors import ItemNotFoundError


class TestRead(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = Context()
        self.repository = MockRepository(True)
        self.controllers = Controllers(self.ctx, self.repository)
        self.login = self.repository.faker.login
        self.user = self.controllers.users.register(self.login)
        self.new_login = self.repository.faker.login
        self.new_user = self.controllers.users.register(self.new_login)
        self.item = self.repository.faker.item

    def test_raises_error_if_not_found(self):
        self.controllers.ctx.add("token", self.user.token)
        with self.assertRaises(ItemNotFoundError):
            self.controllers.items.delete(-1)

    def test_returns_item_if_found(self):
        self.controllers.ctx.add("token", self.user.token)
        item = self.controllers.items.create(self.item)
        self.controllers.ctx.add("token", self.new_user.token)
        result = self.controllers.items.read(item.item_id)
        self.assertEqual(result.item_id, item.item_id)
        self.assertEqual(result.name, self.item.name)
        self.assertEqual(result.icon, self.item.icon)

    def test_user_logged_out_raises_error(self):
        with self.assertRaises(LoggedOut):
            self.controllers.items.read(-1)

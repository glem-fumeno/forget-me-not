import unittest

from api.context import Context
from api.controllers.controllers import Controllers
from api.controllers.mock_repository import MockRepository
from api.errors import Inaccessible, LoggedOut
from api.models.items.errors import ItemExistsError


class TestCreate(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = Context()
        self.repository = MockRepository(True)
        self.controllers = Controllers(self.ctx, self.repository)
        self.login = self.repository.faker.login
        self.user = self.controllers.users.register(self.login)
        self.request = self.repository.faker.item

    def test_name_exists_raises_error(self):
        self.controllers.ctx.add("token", self.user.token)
        self.controllers.items.create(self.request)
        with self.assertRaises(ItemExistsError):
            self.controllers.items.create(self.request)

    def test_new_name_creates_item(self):
        self.controllers.ctx.add("token", self.user.token)
        result = self.controllers.items.create(self.request)
        check = self.controllers.items.read(result.item_id)
        self.assertEqual(result, check)

    def test_user_logged_out_raises_error(self):
        with self.assertRaises(LoggedOut):
            self.controllers.items.create(self.request)

    def test_user_role_raises_error(self):
        user = self.controllers.users.register(self.repository.faker.login)
        self.controllers.ctx.add("token", user.token)
        with self.assertRaises(Inaccessible):
            self.controllers.items.create(self.request)

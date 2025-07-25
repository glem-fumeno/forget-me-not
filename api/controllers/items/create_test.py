import unittest

from api.context import Context
from api.controllers.controllers import Controllers
from api.controllers.faker import Faker
from api.controllers.mock_repository import MockRepository
from api.errors import Inaccessible, LoggedOut
from api.models.items.errors import ItemExistsError


class TestCreate(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = Context()
        self.faker = Faker()
        self.controllers = Controllers(self.ctx, MockRepository())
        self.login = self.faker.login
        self.user = self.controllers.users.register(self.login)
        self.request = self.faker.item

    def test_name_exists_raises_error(self):
        self.ctx.add("token", self.user.token)
        self.controllers.items.create(self.request)
        with self.assertRaises(ItemExistsError):
            self.controllers.items.create(self.request)

    def test_new_name_creates_item(self):
        self.ctx.add("token", self.user.token)
        result = self.controllers.items.create(self.request)
        check = self.controllers.items.read(result.item_id)
        self.assertEqual(result, check)

    def test_user_logged_out_raises_error(self):
        with self.assertRaises(LoggedOut):
            self.controllers.items.create(self.request)

    def test_user_role_raises_error(self):
        user = self.controllers.users.register(self.faker.login)
        self.ctx.add("token", user.token)
        with self.assertRaises(Inaccessible):
            self.controllers.items.create(self.request)

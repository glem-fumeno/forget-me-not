import unittest

from api.context import Context
from api.controllers.controllers import Controllers
from api.controllers.mock_repository import MockRepository
from api.errors import LoggedOut
from api.faker import Faker


class TestSearch(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = Context()
        self.faker = Faker()
        self.controllers = Controllers(self.ctx, MockRepository())
        self.login = self.faker.login
        self.user = self.controllers.users.register(self.login)

    def test_returns_all_items(self):
        self.ctx.add("token", self.user.token)
        for _ in range(12):
            self.controllers.items.create(self.faker.item)
        result = self.controllers.items.search()
        self.assertEqual(len(result.items), 12)
        self.assertEqual(result.count, 12)

    def test_user_logged_out_raises_error(self):
        with self.assertRaises(LoggedOut):
            self.controllers.items.search()

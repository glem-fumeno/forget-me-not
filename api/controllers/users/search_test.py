import unittest

from api.context import Context
from api.controllers.controllers import Controllers
from api.controllers.mock_repository import MockRepository
from api.faker import Faker
from api.models.users.errors import LoggedOut


class TestSearch(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = Context()
        self.faker = Faker()
        self.controllers = Controllers(self.ctx, MockRepository())
        self.login = self.faker.login
        self.user = self.controllers.users.register(self.login)

    def test_logged_out_raises_error(self):
        with self.assertRaises(LoggedOut):
            self.controllers.users.search()

    def test_returns_all_existing_users(self):
        for _ in range(12):
            self.controllers.users.register(self.faker.login)
        self.ctx.add("token", self.user.token)
        result = self.controllers.users.search()
        self.assertEqual(len(result.users), 13)
        self.assertEqual(result.count, 13)

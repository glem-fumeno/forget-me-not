import unittest

from api.context import Context
from api.controllers.controllers import Controllers
from api.controllers.mock_repository import MockRepository
from api.errors import LoggedOut


class TestSearch(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = Context()
        self.repository = MockRepository(True)
        self.controllers = Controllers(self.ctx, self.repository)
        self.login = self.repository.faker.login
        self.user = self.controllers.users.register(self.login)
        self.new_login = self.repository.faker.login
        self.new_user = self.controllers.users.register(self.new_login)

    def test_returns_all_items(self):
        self.controllers.ctx.add("token", self.user.token)
        for _ in range(12):
            self.controllers.items.create(self.repository.faker.item)
        self.controllers.ctx.add("token", self.new_user.token)
        result = self.controllers.items.search()
        self.assertEqual(len(result.items), 12)
        self.assertEqual(result.count, 12)

    def test_user_logged_out_raises_error(self):
        with self.assertRaises(LoggedOut):
            self.controllers.items.search()

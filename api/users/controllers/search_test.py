import unittest

from api.context import Context
from api.users.controllers.core_test import UserTestRepository
from api.users.controllers.search import UserSearchController
from api.users.schemas.errors import LoggedOut


class TestSearch(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = UserTestRepository()
        user_id = self.repository.email_map["alice.anderson@example.com"]
        self.ctx = Context().add("token", self.repository.login(user_id))
        self.controller = UserSearchController(self.ctx, self.repository)

    def test_returns_all_existing_users(self):
        result = self.controller.run()
        self.assertEqual(len(result.users), 2)
        self.assertEqual(result.count, 2)

    def test_logged_out_raises_error(self):
        self.controller.ctx = self.controller.ctx.add("token", "")

        with self.assertRaises(LoggedOut):
            self.controller.run()

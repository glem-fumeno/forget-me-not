import unittest

from api.context import Context
from api.controllers.items.search import ItemSearchController
from api.controllers.mock_repository import MockRepository
from api.errors import LoggedOut


class TestSearch(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = MockRepository()
        user_id = self.repository.email_map["alice.anderson@example.com"]
        self.ctx = Context().add("token", self.repository.login(user_id))
        self.controller = ItemSearchController(self.ctx, self.repository)

    def test_returns_all_items(self):
        user_id = self.repository.email_map["bob.baker@example.com"]
        self.controller.ctx = self.controller.ctx.add(
            "token", self.repository.login(user_id)
        )
        result = self.controller.run()
        self.assertEqual(len(result.items), 5)
        self.assertEqual(result.count, 5)

    def test_user_logged_out_raises_error(self):
        self.controller.ctx = self.controller.ctx.add("token", "")
        with self.assertRaises(LoggedOut):
            self.controller.run()

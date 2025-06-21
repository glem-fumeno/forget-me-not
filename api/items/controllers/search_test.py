import unittest

from api.context import Context
from api.errors import LoggedOut
from api.items.controllers.core_test import ItemTestRepository
from api.items.controllers.search import ItemSearchController


class TestSearch(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = ItemTestRepository()
        user_id = self.repository.email_map["alice.anderson@example.com"]
        self.ctx = Context().add("token", self.repository.login(user_id))
        self.controller = ItemSearchController(self.ctx, self.repository)

    def test_returns_all_items(self):
        user_id = self.repository.email_map["bob.baker@example.com"]
        self.controller.ctx = self.controller.ctx.add(
            "token", self.repository.login(user_id)
        )
        result = self.controller.run()
        self.assertEqual(len(result.items), 2)
        self.assertEqual(result.count, 2)

    def test_user_logged_out_raises_error(self):
        self.controller.ctx = self.controller.ctx.add("token", "")
        with self.assertRaises(LoggedOut):
            self.controller.run()

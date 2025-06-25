import unittest

from api.carts.controllers.core_test import CartTestRepository
from api.carts.controllers.search import CartSearchController
from api.context import Context
from api.errors import LoggedOut


class TestSearch(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = CartTestRepository()
        user_id = self.repository.email_map["alice.anderson@example.com"]
        self.ctx = Context().add("token", self.repository.login(user_id))
        self.controller = CartSearchController(self.ctx, self.repository)

    def test_returns_all_carts(self):
        user_id = self.repository.email_map["bob.baker@example.com"]
        self.controller.ctx = self.controller.ctx.add(
            "token", self.repository.login(user_id)
        )
        result = self.controller.run()
        self.assertEqual(len(result.carts), 1)
        self.assertEqual(result.count, 1)

    def test_user_logged_out_raises_error(self):
        self.controller.ctx = self.controller.ctx.add("token", "")
        with self.assertRaises(LoggedOut):
            self.controller.run()

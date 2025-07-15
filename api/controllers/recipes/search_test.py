import unittest

from api.context import Context
from api.errors import LoggedOut
from api.controllers.recipes.core_test import RecipeTestRepository
from api.controllers.recipes.search import RecipeSearchController


class TestSearch(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = RecipeTestRepository()
        user_id = self.repository.email_map["alice.anderson@example.com"]
        self.ctx = Context().add("token", self.repository.login(user_id))
        self.controller = RecipeSearchController(self.ctx, self.repository)

    def test_returns_all_recipes(self):
        user_id = self.repository.email_map["bob.baker@example.com"]
        self.controller.ctx = self.controller.ctx.add(
            "token", self.repository.login(user_id)
        )
        result = self.controller.run()
        self.assertEqual(len(result.recipes), 1)
        self.assertEqual(result.count, 1)

    def test_user_logged_out_raises_error(self):
        self.controller.ctx = self.controller.ctx.add("token", "")
        with self.assertRaises(LoggedOut):
            self.controller.run()

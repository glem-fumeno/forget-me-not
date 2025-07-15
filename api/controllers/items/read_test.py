import unittest

from api.context import Context
from api.errors import LoggedOut
from api.controllers.items.core_test import ItemTestRepository
from api.controllers.items.read import ItemReadController
from api.models.items.errors import ItemNotFoundError


class TestRead(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = ItemTestRepository()
        user_id = self.repository.email_map["alice.anderson@example.com"]
        self.ctx = Context().add("token", self.repository.login(user_id))
        self.controller = ItemReadController(self.ctx, self.repository)

    def test_raises_error_if_not_found(self):
        with self.assertRaises(ItemNotFoundError):
            self.controller.run(-1)

    def test_returns_item_if_found(self):
        user_id = self.repository.email_map["bob.baker@example.com"]
        self.controller.ctx = self.controller.ctx.add(
            "token", self.repository.login(user_id)
        )
        item_id = self.repository.item_name_map["milk"]
        model = self.repository.item_map[item_id]
        result = self.controller.run(item_id)
        self.assertEqual(result.item_id, item_id)
        self.assertEqual(result.name, model.name)
        self.assertEqual(result.icon, model.icon)

    def test_user_logged_out_raises_error(self):
        self.controller.ctx = self.controller.ctx.add("token", "")
        with self.assertRaises(LoggedOut):
            self.controller.run(-1)

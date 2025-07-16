import unittest

from api.context import Context
from api.controllers.items.delete import ItemDeleteController
from api.controllers.mock_repository import MockRepository
from api.errors import Inaccessible, LoggedOut
from api.models.items.errors import ItemNotFoundError


class TestDelete(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = MockRepository()
        user_id = self.repository.email_map["alice.anderson@example.com"]
        self.ctx = Context().add("token", self.repository.login(user_id))
        self.controller = ItemDeleteController(self.ctx, self.repository)

    def test_raises_error_if_not_found(self):
        with self.assertRaises(ItemNotFoundError):
            self.controller.run(-1)

    def test_found_removes_item(self):
        item_id = self.repository.item_name_map["milk"]
        item = self.repository.item_map[item_id]
        result = self.controller.run(item_id)
        self.assertNotIn(item_id, self.repository.item_map)
        self.assertEqual(item.item_id, result.item_id)
        self.assertEqual(item.name, result.name)
        self.assertEqual(item.icon, result.icon)

    def test_user_logged_out_raises_error(self):
        self.controller.ctx = self.controller.ctx.add("token", "")
        with self.assertRaises(LoggedOut):
            self.controller.run(-1)

    def test_user_role_raises_error(self):
        user_id = self.repository.email_map["bob.baker@example.com"]
        self.controller.ctx = self.controller.ctx.add(
            "token", self.repository.login(user_id)
        )
        with self.assertRaises(Inaccessible):
            self.controller.run(-1)

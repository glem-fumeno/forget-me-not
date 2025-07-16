import unittest

from api.context import Context
from api.controllers.items.update import ItemUpdateController
from api.controllers.mock_repository import MockRepository
from api.errors import Inaccessible, LoggedOut
from api.models.items.errors import ItemExistsError, ItemNotFoundError
from api.models.items.requests import ItemUpdateRequest


class TestUpdate(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = MockRepository()
        user_id = self.repository.email_map["alice.anderson@example.com"]
        self.ctx = Context().add("token", self.repository.login(user_id))
        self.controller = ItemUpdateController(self.ctx, self.repository)

    def test_raises_error_if_not_found(self):
        request = ItemUpdateRequest()
        with self.assertRaises(ItemNotFoundError):
            self.controller.run(-1, request)

    def test_updates_name(self):
        request = ItemUpdateRequest(name="milk-carton")
        item_id = self.repository.item_name_map["milk"]
        model = self.repository.item_map[item_id].copy()
        result = self.controller.run(item_id, request)
        new_model = self.repository.item_map[item_id].copy()

        self.assertEqual(model.item_id, new_model.item_id)
        self.assertNotEqual(model.name, new_model.name)
        self.assertEqual(model.icon, new_model.icon)

        self.assertEqual(result.item_id, item_id)
        self.assertEqual(result.name, request.name)
        self.assertEqual(result.icon, model.icon)

    def test_raises_error_if_name_exists(self):
        request = ItemUpdateRequest(name="rice")
        item_id = self.repository.item_name_map["milk"]
        with self.assertRaises(ItemExistsError):
            self.controller.run(item_id, request)

    def test_raises_no_error_if_email_taken_is_self(self):
        request = ItemUpdateRequest(name="rice")
        item_id = self.repository.item_name_map["rice"]
        self.controller.run(item_id, request)

    def test_updates_icon(self):
        request = ItemUpdateRequest(
            icon="https://img.icons8.com/pulsar-line/96/milk-carton.png"
        )
        item_id = self.repository.item_name_map["milk"]
        model = self.repository.item_map[item_id].copy()
        result = self.controller.run(item_id, request)
        new_model = self.repository.item_map[item_id].copy()

        self.assertEqual(model.item_id, new_model.item_id)
        self.assertEqual(model.name, new_model.name)
        self.assertNotEqual(model.icon, new_model.icon)

        self.assertEqual(result.item_id, item_id)
        self.assertEqual(result.name, model.name)
        self.assertEqual(result.icon, request.icon)

    def test_user_logged_out_raises_error(self):
        self.controller.ctx = self.controller.ctx.add("token", "")
        with self.assertRaises(LoggedOut):
            self.controller.run(-1, ItemUpdateRequest())

    def test_user_role_raises_error(self):
        user_id = self.repository.email_map["bob.baker@example.com"]
        self.controller.ctx = self.controller.ctx.add(
            "token", self.repository.login(user_id)
        )
        with self.assertRaises(Inaccessible):
            self.controller.run(-1, ItemUpdateRequest())

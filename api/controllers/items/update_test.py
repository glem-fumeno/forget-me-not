import unittest

from api.context import Context
from api.controllers.controllers import Controllers
from api.controllers.mock_repository import MockRepository
from api.errors import Inaccessible, LoggedOut
from api.models.items.errors import ItemExistsError, ItemNotFoundError
from api.models.items.requests import ItemUpdateRequest


class TestUpdate(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = Context()
        self.repository = MockRepository(True)
        self.controllers = Controllers(self.ctx, self.repository)
        self.login = self.repository.faker.login
        self.user = self.controllers.users.register(self.login)
        self.controllers.ctx.add("token", self.user.token)
        self.item = self.controllers.items.create(self.repository.faker.item)
        self.new_item = self.controllers.items.create(
            self.repository.faker.item
        )
        self.request = ItemUpdateRequest()

    def test_raises_error_if_not_found(self):
        with self.assertRaises(ItemNotFoundError):
            self.controllers.items.update(-1, self.request)

    def test_updates_name(self):
        self.request.name = self.repository.faker.noun
        result = self.controllers.items.update(self.item.item_id, self.request)
        check = self.controllers.items.read(self.item.item_id)
        self.assertEqual(result, check)

        self.assertEqual(result.item_id, self.item.item_id)
        self.assertEqual(result.name, self.request.name)
        self.assertEqual(result.icon, self.item.icon)

    def test_raises_error_if_name_exists(self):
        self.request.name = self.new_item.name
        with self.assertRaises(ItemExistsError):
            self.controllers.items.update(self.item.item_id, self.request)

    def test_raises_no_error_if_email_taken_is_self(self):
        self.request.name = self.new_item.name
        self.controllers.items.update(self.new_item.item_id, self.request)

    def test_updates_icon(self):
        self.request.icon = self.repository.faker.icon
        result = self.controllers.items.update(self.item.item_id, self.request)
        check = self.controllers.items.read(self.item.item_id)
        self.assertEqual(result, check)

        self.assertEqual(result.item_id, self.item.item_id)
        self.assertEqual(result.name, self.item.name)
        self.assertEqual(result.icon, self.request.icon)

    def test_user_logged_out_raises_error(self):
        self.controllers.ctx.add("token", "")
        with self.assertRaises(LoggedOut):
            self.controllers.items.update(-1, self.request)

    def test_user_role_raises_error(self):
        user = self.controllers.users.register(self.repository.faker.login)
        self.controllers.ctx.add("token", user.token)
        with self.assertRaises(Inaccessible):
            self.controllers.items.update(-1, self.request)

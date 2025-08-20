from api.models.items.errors import ItemExistsError, ItemNotFoundError
from api.models.items.requests import ItemUpdateRequest
from api.test_case import TestCase


class TestUpdate(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.item = self.controllers.items.create(self.faker.item)
        self.new_item = self.controllers.items.create(self.faker.item)
        self.request = ItemUpdateRequest()

    def test_raises_error_if_not_found(self):
        with self.assertRaises(ItemNotFoundError):
            self.controllers.items.update(-1, self.request)

    def test_updates_name(self):
        self.request.name = self.faker.noun
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
        self.request.icon = self.faker.icon
        result = self.controllers.items.update(self.item.item_id, self.request)
        check = self.controllers.items.read(self.item.item_id)
        self.assertEqual(result, check)

        self.assertEqual(result.item_id, self.item.item_id)
        self.assertEqual(result.name, self.item.name)
        self.assertEqual(result.icon, self.request.icon)

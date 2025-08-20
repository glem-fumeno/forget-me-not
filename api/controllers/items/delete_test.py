from api.models.items.errors import ItemNotFoundError
from api.test_case import TestCase


class TestDelete(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.item = self.faker.item

    def test_raises_error_if_not_found(self):
        with self.assertRaises(ItemNotFoundError):
            self.controllers.items.delete(-1)

    def test_found_removes_item(self):
        item = self.controllers.items.create(self.item)
        result = self.controllers.items.delete(item.item_id)
        self.assertEqual(item, result)
        with self.assertRaises(ItemNotFoundError):
            self.controllers.items.read(item.item_id)

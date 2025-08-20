from api.models.items.errors import ItemNotFoundError
from api.test_case import TestCase


class TestRead(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.item = self.faker.item

    def test_raises_error_if_not_found(self):
        with self.assertRaises(ItemNotFoundError):
            self.controllers.items.delete(-1)

    def test_returns_item_if_found(self):
        item = self.controllers.items.create(self.item)
        result = self.controllers.items.read(item.item_id)
        self.assertEqual(result.item_id, item.item_id)
        self.assertEqual(result.name, self.item.name)
        self.assertEqual(result.icon, self.item.icon)

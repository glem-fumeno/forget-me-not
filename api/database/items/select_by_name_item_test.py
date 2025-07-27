import unittest

from api.context import Context
from api.database.repository import DatabaseRepository
from api.faker import Faker


class TestSelectItemByName(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseRepository(Context(), ":memory:")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.faker = Faker()
        self.item = self.faker.item_model

    def test_returns_none_when_no_item(self):
        result = self.repository.items.select_item_by_name("")
        self.assertIsNone(result)

    def test_returns_item_when_found(self):
        self.repository.items.insert_item(self.item)
        result = self.repository.items.select_item_by_name(self.item.name)
        self.assertEqual(result, self.item.item_id)

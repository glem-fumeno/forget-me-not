import unittest

from api.context import Context
from api.database.repository import DatabaseRepository
from api.faker import Faker


class TestSelectItem(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.faker = Faker()
        self.item = self.faker.item_model

    def test_returns_all_items(self):
        self.repository.items.insert_item(self.item)
        for _ in range(12):
            self.repository.items.insert_item(self.faker.item_model)
        result = self.repository.items.select_items()
        self.assertEqual(len(result), 13)
        self.assertEqual(result[self.item.item_id], self.item)

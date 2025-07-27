import unittest

from api.context import Context
from api.database.repository import DatabaseRepository
from api.faker import Faker


class TestInsertItem(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseRepository(Context(), ":memory:")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.faker = Faker()
        self.item = self.faker.item_model

    def test_changes_item_id(self):
        self.repository.items.insert_item(self.item)
        self.assertNotEqual(self.item.item_id, -1)

    def test_inserts_item_to_db(self):
        self.repository.items.insert_item(self.item)
        result = self.repository.items.select_item(self.item.item_id)
        self.assertIsNotNone(result)

import unittest

from api.context import Context
from api.database.repository import DatabaseRepository
from api.faker import Faker


class TestDeleteItem(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.faker = Faker()
        self.item = self.faker.item_model

    def test_deletes_item_when_found(self):
        self.repository.items.insert_item(self.item)
        self.repository.items.delete_item(self.item.item_id)
        result = self.repository.items.select_item(self.item.item_id)
        self.assertIsNone(result)

import unittest

from api.context import Context
from api.database.repository import DatabaseRepository
from api.faker import Faker


class TestUpdateItem(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseRepository(Context(), ":memory:")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.faker = Faker()
        self.item = self.faker.item_model

    def test_updates_item_in_db(self):
        self.repository.items.insert_item(self.item)
        model = self.faker.item_model
        model.item_id = self.item.item_id
        self.repository.items.update_item(model)
        result = self.repository.items.select_item(self.item.item_id)
        self.assertEqual(result, model)

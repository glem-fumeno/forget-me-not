import unittest

from api.context import Context
from api.database.test_repository import DatabaseTestRepository


class TestSelectItemByName(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseTestRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.repository.initialize_test_cases()

    def test_returns_none_when_no_item(self):
        result = self.repository.items.select_item_by_name("needle")
        self.assertIsNone(result)

    def test_returns_item_when_found(self):
        item_id = self.repository.item_name_map["milk"]
        result = self.repository.items.select_item_by_name("milk")
        self.assertEqual(result, item_id)

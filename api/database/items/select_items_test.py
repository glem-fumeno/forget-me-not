import unittest

from api.context import Context
from api.database.test_repository import DatabaseTestRepository


class TestSelectItem(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseTestRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.repository.initialize_test_cases()

    def test_returns_all_items(self):
        result = self.repository.items.select_items()
        self.assertEqual(len(result), 5)
        self.assertIn(self.repository.item_name_map["milk"], result)
        self.assertIn(self.repository.item_name_map["rice"], result)

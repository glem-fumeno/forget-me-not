import unittest

from api.items.database.core_test import ItemDatabaseTestRepository


class TestSelectItem(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = ItemDatabaseTestRepository("test.db")
        self.repository.connect()
        self.repository.initialize_test_cases()

    def tearDown(self) -> None:
        self.repository.connection.rollback()
        self.repository.connection.close()

    def test_returns_all_items(self):
        result = self.repository.select_items()
        self.assertEqual(len(result), 2)
        self.assertIn(self.repository.item_name_map["milk"], result)
        self.assertIn(self.repository.item_name_map["rice"], result)

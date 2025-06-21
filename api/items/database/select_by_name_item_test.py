import unittest

from api.items.database.core_test import ItemDatabaseTestRepository


class TestSelectItemByName(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = ItemDatabaseTestRepository("test.db")
        self.repository.connect()
        self.repository.initialize_test_cases()

    def tearDown(self) -> None:
        self.repository.connection.rollback()
        self.repository.connection.close()

    def test_returns_none_when_no_item(self):
        result = self.repository.select_item_by_name("soap")
        self.assertIsNone(result)

    def test_returns_item_when_found(self):
        item_id = self.repository.item_name_map["milk"]
        result = self.repository.select_item_by_name("milk")
        self.assertEqual(result, item_id)

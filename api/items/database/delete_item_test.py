import unittest

from api.items.database.core_test import ItemDatabaseTestRepository


class TestDeleteItem(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = ItemDatabaseTestRepository("test.db")
        self.repository.connect()
        self.repository.initialize_test_cases()

    def tearDown(self) -> None:
        self.repository.connection.rollback()
        self.repository.connection.close()

    def test_returns_item_when_found(self):
        item_id = self.repository.item_name_map["milk"]
        self.repository.delete_item(item_id)
        result = self.repository.cursor.execute(
            """
            SELECT item_id_ FROM items_ WHERE item_id_ = ?
            """,
            (item_id,),
        )
        self.assertIsNone(result.fetchone())

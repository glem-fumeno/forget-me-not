import unittest

from api.context import Context
from api.database.test_repository import DatabaseTestRepository


class TestDeleteItem(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseTestRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.repository.initialize_test_cases()

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

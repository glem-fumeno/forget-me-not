import unittest

from api.context import Context
from api.database.test_repository import DatabaseTestRepository


class TestDeleteCartItem(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseTestRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.repository.initialize_test_cases()

    def test_inserts_cart_item_to_db(self):
        user_id = self.repository.email_map["alice.anderson@example.com"]
        cart_id = self.repository.cart_name_map[user_id, "groceries"]
        item_id = self.repository.item_name_map["milk"]
        self.repository.delete_cart_item(cart_id, item_id)
        result = self.repository.cursor.execute(
            """
            SELECT cart_id_
            FROM carts_items_
            WHERE cart_id_ = ? AND item_id_ = ?
            """,
            (cart_id, item_id),
        )
        self.assertIsNone(result.fetchone())

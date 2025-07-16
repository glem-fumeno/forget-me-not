import unittest

from api.context import Context
from api.database.test_repository import DatabaseTestRepository


class TestDeleteCart(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseTestRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.repository.initialize_test_cases()

    def test_returns_cart_when_found(self):
        user_id = self.repository.email_map["alice.anderson@example.com"]
        cart_id = self.repository.cart_name_map[user_id, "groceries"]
        self.repository.delete_cart(cart_id)
        result = self.repository.cursor.execute(
            """
            SELECT cart_id_ FROM carts_ WHERE cart_id_ = ?
            """,
            (cart_id,),
        )
        self.assertIsNone(result.fetchone())

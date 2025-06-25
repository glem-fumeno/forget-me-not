import unittest

from api.carts.database.core_test import CartDatabaseTestRepository
from api.context import Context


class TestDeleteCart(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = CartDatabaseTestRepository(Context(), "test.db")
        self.repository.connect()
        self.repository.initialize_test_cases()

    def tearDown(self) -> None:
        self.repository.connection.rollback()
        self.repository.connection.close()

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

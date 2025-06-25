import unittest

from api.carts.database.core_test import CartDatabaseTestRepository
from api.context import Context


class TestSelectCarts(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = CartDatabaseTestRepository(Context(), "test.db")
        self.repository.connect()
        self.repository.initialize_test_cases()

    def tearDown(self) -> None:
        self.repository.connection.rollback()
        self.repository.connection.close()

    def test_returns_all_carts(self):
        user_id = self.repository.email_map["alice.anderson@example.com"]
        result = self.repository.select_carts(user_id)
        self.assertEqual(len(result), 2)
        self.assertIn(
            self.repository.cart_name_map[user_id, "groceries"], result
        )
        self.assertIn(
            self.repository.cart_name_map[user_id, "groceries"], result
        )

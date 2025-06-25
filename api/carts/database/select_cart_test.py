import unittest

from api.carts.database.core_test import CartDatabaseTestRepository
from api.context import Context


class TestSelectCart(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = CartDatabaseTestRepository(Context(), "test.db")
        self.repository.connect()
        self.repository.initialize_test_cases()

    def tearDown(self) -> None:
        self.repository.connection.rollback()
        self.repository.connection.close()

    def test_returns_none_when_no_cart(self):
        user_id = self.repository.email_map["bob.baker@example.com"]
        owner_id = self.repository.email_map["alice.anderson@example.com"]
        cart_id = self.repository.cart_name_map[owner_id, "gift for bob"]
        result = self.repository.select_cart(user_id, cart_id)
        self.assertIsNone(result)

    def test_returns_cart_when_found(self):
        user_id = self.repository.email_map["alice.anderson@example.com"]
        cart_id = self.repository.cart_name_map[user_id, "groceries"]
        result = self.repository.select_cart(user_id, cart_id)
        self.assertEqual(result, self.repository.cart_map[cart_id])

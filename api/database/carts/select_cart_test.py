import unittest

from api.context import Context
from api.database.test_repository import DatabaseTestRepository


class TestSelectCart(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseTestRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.repository.initialize_test_cases()

    def test_returns_none_when_no_cart(self):
        user_id = self.repository.email_map["bob.baker@example.com"]
        owner_id = self.repository.email_map["alice.anderson@example.com"]
        cart_id = self.repository.cart_name_map[owner_id, "gift for bob"]
        result = self.repository.carts.select_cart(user_id, cart_id)
        self.assertIsNone(result)

    def test_returns_cart_when_found(self):
        user_id = self.repository.email_map["alice.anderson@example.com"]
        cart_id = self.repository.cart_name_map[user_id, "groceries"]
        result = self.repository.carts.select_cart(user_id, cart_id)
        self.assertEqual(result, self.repository.cart_map[cart_id])

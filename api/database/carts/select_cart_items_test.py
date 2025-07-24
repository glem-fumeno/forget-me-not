import unittest

from api.context import Context
from api.database.test_repository import DatabaseTestRepository


class TestSelectCartItems(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseTestRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.repository.initialize_test_cases()

    def test_returns_all_cart_items(self):
        user_id = self.repository.email_map["alice.anderson@example.com"]
        cart_id = self.repository.cart_name_map[user_id, "groceries"]
        result = self.repository.carts.select_cart_items(cart_id)
        self.assertEqual(len(result), 2)
        self.assertIn(self.repository.item_name_map["milk"], result)
        self.assertIn(self.repository.item_name_map["rice"], result)

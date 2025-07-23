import unittest

from api.context import Context
from api.database.test_repository import DatabaseTestRepository


class TestReadUserCart(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseTestRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.repository.initialize_test_cases()

    def test_reads_cart_from_db(self):
        user_id = self.repository.email_map["alice.anderson@example.com"]
        cart_id = self.repository.cart_name_map[user_id, "groceries"]
        self.repository.update_user_cart(user_id, cart_id)
        result = self.repository.select_user_cart(user_id)
        self.assertEqual(result, cart_id)

    def test_returns_none_if_not_found(self):
        result = self.repository.select_user_cart(-1)
        self.assertIsNone(result)

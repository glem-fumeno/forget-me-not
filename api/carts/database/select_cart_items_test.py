import unittest

from api.carts.database.core_test import CartDatabaseTestRepository


class TestSelectCartItems(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = CartDatabaseTestRepository("test.db")
        self.repository.connect()
        self.repository.initialize_test_cases()

    def tearDown(self) -> None:
        self.repository.connection.rollback()
        self.repository.connection.close()

    def test_returns_all_cart_items(self):
        user_id = self.repository.email_map["alice.anderson@example.com"]
        cart_id = self.repository.cart_name_map[user_id, "groceries"]
        result = self.repository.select_cart_items(cart_id)
        self.assertEqual(len(result), 2)
        self.assertEqual(
            self.repository.item_map[self.repository.item_name_map["milk"]],
            result[0]
        )
        self.assertEqual(
            self.repository.item_map[self.repository.item_name_map["rice"]],
            result[1]
        )

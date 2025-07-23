import unittest

from api.context import Context
from api.database.test_repository import DatabaseTestRepository
from api.models.carts.models import CartModel


class TestUpdateUserCart(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseTestRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.repository.initialize_test_cases()

    def test_updates_cart_in_db(self):
        user_id = self.repository.email_map["alice.anderson@example.com"]
        cart_id = self.repository.cart_name_map[user_id, "groceries"]
        self.repository.update_user_cart(user_id, cart_id)
        result = self.repository.cursor.execute(
            """
            SELECT cart_id_ FROM users_ WHERE user_id_ = ?
            """,
            (user_id,),
        )
        self.assertEqual(result.fetchone()[0], cart_id)

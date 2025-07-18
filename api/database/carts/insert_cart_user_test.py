import unittest

from api.context import Context
from api.database.test_repository import DatabaseTestRepository
from api.models.carts.models import CartUserModel


class TestInsertCartUser(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseTestRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.repository.initialize_test_cases()

    def test_inserts_cart_session_to_db(self):
        owner_id = self.repository.email_map["alice.anderson@example.com"]
        user_id = self.repository.email_map["bob.baker@example.com"]
        cart_id = self.repository.cart_name_map[owner_id, "gift for bob"]
        model = CartUserModel(cart_id=cart_id, user_id=user_id)
        self.repository.insert_cart_user(model)
        result = self.repository.cursor.execute(
            """
            SELECT cart_id_
            FROM carts_users_
            WHERE user_id_ = ? AND cart_id_ = ?
            """,
            (model.user_id, model.cart_id),
        )
        self.assertEqual(model.cart_id, result.fetchone()[0])

import unittest

from api.carts.database.core_test import CartDatabaseTestRepository
from api.carts.schemas.models import CartUserModel


class TestInsertCartUser(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = CartDatabaseTestRepository("test.db")
        self.repository.connect()
        self.repository.initialize_test_cases()

    def tearDown(self) -> None:
        self.repository.connection.rollback()
        self.repository.connection.close()

    def test_inserts_cart_session_to_db(self):
        owner_id = self.repository.email_map["alice.anderson@example.com"]
        user_id = self.repository.email_map["bob.baker@example.com"]
        cart_id = self.repository.cart_name_map[owner_id, "gift for bob"]
        model = CartUserModel(cart_id, user_id)
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

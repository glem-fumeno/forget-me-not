import unittest

from api.carts.database.core_test import CartDatabaseTestRepository
from api.carts.schemas.models import CartModel
from api.context import Context


class TestInsertCart(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = CartDatabaseTestRepository(Context(), "test.db")
        self.repository.connect()
        self.repository.initialize_test_cases()

    def tearDown(self) -> None:
        self.repository.connection.rollback()
        self.repository.connection.close()

    def test_changes_cart_id(self):
        model = CartModel(
            cart_id=-1,
            name="office supplies",
            icon="https://img.icons8.com/pulsar-line/96/length-1.png",
        )
        user_id = self.repository.email_map["alice.anderson@example.com"]
        self.repository.insert_cart(user_id, model)
        self.assertNotEqual(model.cart_id, -1)

    def test_inserts_cart_to_db(self):
        model = CartModel(
            cart_id=-1,
            name="office supplies",
            icon="https://img.icons8.com/pulsar-line/96/length-1.png",
        )
        user_id = self.repository.email_map["alice.anderson@example.com"]
        self.repository.insert_cart(user_id, model)
        result = self.repository.cursor.execute(
            """
            SELECT cart_id_ FROM carts_ WHERE cart_id_ = ?
            """,
            (model.cart_id,),
        )
        self.assertEqual(model.cart_id, result.fetchone()[0])

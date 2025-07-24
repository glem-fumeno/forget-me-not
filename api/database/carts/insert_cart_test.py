import unittest

from api.context import Context
from api.database.test_repository import DatabaseTestRepository
from api.models.carts.models import CartModel


class TestInsertCart(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseTestRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.repository.initialize_test_cases()

    def test_changes_cart_id(self):
        model = CartModel(
            cart_id=-1,
            name="office supplies",
            icon="https://img.icons8.com/pulsar-line/96/length-1.png",
        )
        user_id = self.repository.email_map["alice.anderson@example.com"]
        self.repository.carts.insert_cart(user_id, model)
        self.assertNotEqual(model.cart_id, -1)

    def test_inserts_cart_to_db(self):
        model = CartModel(
            cart_id=-1,
            name="office supplies",
            icon="https://img.icons8.com/pulsar-line/96/length-1.png",
        )
        user_id = self.repository.email_map["alice.anderson@example.com"]
        self.repository.carts.insert_cart(user_id, model)
        result = self.repository.cursor.execute(
            """
            SELECT cart_id_ FROM carts_ WHERE cart_id_ = ?
            """,
            (model.cart_id,),
        )
        self.assertEqual(model.cart_id, result.fetchone()[0])

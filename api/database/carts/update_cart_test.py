import unittest

from api.context import Context
from api.database.test_repository import DatabaseTestRepository
from api.models.carts.models import CartModel


class TestUpdateCart(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseTestRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.repository.initialize_test_cases()

    def test_updates_cart_in_db(self):
        user_id = self.repository.email_map["alice.anderson@example.com"]
        cart_id = self.repository.cart_name_map[user_id, "groceries"]
        model = CartModel(
            cart_id=cart_id,
            name="shopping",
            icon="https://img.icons8.com/pulsar-line/96/shopping-trolley.png",
        )
        self.repository.update_cart(model)
        result = self.repository.cursor.execute(
            """
            SELECT cart_id_, name_, icon_ FROM carts_ WHERE cart_id_ = ?
            """,
            (cart_id,),
        )
        new_model = CartModel.from_db(result.description, result.fetchone())
        self.assertEqual(model, new_model)

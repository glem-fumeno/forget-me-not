import unittest

from api.carts.database.core_test import CartDatabaseTestRepository
from api.carts.schemas.models import CartModel


class TestUpdateCart(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = CartDatabaseTestRepository("test.db")
        self.repository.connect()
        self.repository.initialize_test_cases()

    def tearDown(self) -> None:
        self.repository.connection.rollback()
        self.repository.connection.close()

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

import unittest

from api.context import Context
from api.database.repository import DatabaseRepository
from api.faker import Faker


class TestInsertCart(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseRepository(Context(), ":memory:")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.faker = Faker()
        self.cart = self.faker.cart_model

    def test_changes_cart_id(self):
        self.repository.carts.insert_cart(self.cart)
        self.assertNotEqual(self.cart.cart_id, -1)

    def test_inserts_cart_to_db(self):
        self.repository.carts.insert_cart(self.cart)
        result = self.repository.carts.select_cart(self.cart.cart_id)
        self.assertIsNotNone(result)

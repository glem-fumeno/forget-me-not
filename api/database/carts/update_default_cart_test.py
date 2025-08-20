import unittest

from api.context import Context
from api.database.repository import DatabaseRepository
from api.faker import Faker


class TestUpdateDefaultCart(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseRepository(Context(), ":memory:")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.faker = Faker()
        self.cart = self.faker.cart_model

    def test_updates_cart_in_db(self):
        self.repository.carts.insert_cart(self.cart)
        self.repository.carts.update_default_cart(self.cart.cart_id)
        result = self.repository.carts.select_default_cart()
        assert result is not None
        self.assertEqual(result.cart_id, self.cart.cart_id)

import unittest

from api.context import Context
from api.database.repository import DatabaseRepository
from api.faker import Faker


class TestDeleteCart(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.faker = Faker()
        self.user = self.faker.user_model
        self.cart = self.faker.cart_model

    def test_deletes_cart_when_found(self):
        self.repository.users.insert_user(self.user)
        self.repository.carts.insert_cart(self.user.user_id, self.cart)
        self.repository.carts.delete_cart(self.cart.cart_id)
        result = self.repository.carts.select_cart(
            self.user.user_id, self.cart.cart_id
        )
        self.assertIsNone(result)

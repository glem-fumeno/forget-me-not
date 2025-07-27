import unittest

from api.context import Context
from api.database.repository import DatabaseRepository
from api.faker import Faker


class TestSelectCart(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.faker = Faker()
        self.user = self.faker.user_model
        self.repository.users.insert_user(self.user)
        self.new_user = self.faker.user_model
        self.repository.users.insert_user(self.new_user)
        self.cart = self.faker.cart_model

    def test_returns_none_when_no_cart(self):
        self.repository.carts.insert_cart(self.user.user_id, self.cart)
        result = self.repository.carts.select_cart(
            self.new_user.user_id, self.cart.cart_id
        )
        self.assertIsNone(result)

    def test_returns_cart_when_found(self):
        self.repository.carts.insert_cart(self.user.user_id, self.cart)
        result = self.repository.carts.select_cart(
            self.user.user_id, self.cart.cart_id
        )
        self.assertEqual(result, self.cart)

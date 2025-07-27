import unittest

from api.context import Context
from api.database.repository import DatabaseRepository
from api.faker import Faker


class TestSelectCarts(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseRepository(Context(), ":memory:")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.faker = Faker()
        self.user = self.faker.user_model
        self.repository.users.insert_user(self.user)
        self.new_user = self.faker.user_model
        self.repository.users.insert_user(self.new_user)
        self.cart = self.faker.cart_model

    def test_returns_all_carts(self):
        self.repository.carts.insert_cart(self.user.user_id, self.cart)
        for _ in range(12):
            self.repository.carts.insert_cart(
                self.user.user_id, self.faker.cart_model
            )
        for _ in range(5):
            self.repository.carts.insert_cart(
                self.new_user.user_id, self.faker.cart_model
            )
        result = self.repository.carts.select_carts(self.user.user_id)
        self.assertEqual(len(result), 13)
        self.assertEqual(result[self.cart.cart_id], self.cart)

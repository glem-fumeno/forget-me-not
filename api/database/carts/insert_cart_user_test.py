import unittest

from api.context import Context
from api.database.repository import DatabaseRepository
from api.faker import Faker
from api.models.carts.models import CartUserModel


class TestInsertCartUser(unittest.TestCase):
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

    def test_adds_cart_to_user_to_db(self):
        self.repository.carts.insert_cart(self.user.user_id, self.cart)
        model = CartUserModel(
            cart_id=self.cart.cart_id, user_id=self.new_user.user_id
        )
        self.repository.carts.insert_cart_user(model)
        result = self.repository.carts.select_cart(
            self.new_user.user_id, self.cart.cart_id
        )
        self.assertIsNotNone(result)

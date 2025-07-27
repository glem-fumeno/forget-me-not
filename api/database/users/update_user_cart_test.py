import unittest

from api.context import Context
from api.database.repository import DatabaseRepository
from api.faker import Faker


class TestUpdateUserCart(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseRepository(Context(), ":memory:")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.faker = Faker()
        self.user = self.faker.user_model
        self.cart = self.faker.cart_model

    def test_updates_cart_in_db(self):
        self.repository.users.insert_user(self.user)
        self.repository.carts.insert_cart(self.user.user_id, self.cart)
        self.repository.users.update_user_cart(
            self.user.user_id, self.cart.cart_id
        )
        result = self.repository.users.select_user(self.user.user_id)
        assert result is not None
        self.assertEqual(result.cart_id, self.cart.cart_id)

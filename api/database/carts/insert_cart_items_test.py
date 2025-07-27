import unittest

from api.context import Context
from api.database.repository import DatabaseRepository
from api.faker import Faker


class TestInsertCartItem(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.faker = Faker()
        self.item = self.faker.item_model
        self.user = self.faker.user_model
        self.cart = self.faker.cart_model

    def test_inserts_cart_item_to_db(self):
        self.repository.users.insert_user(self.user)
        self.repository.carts.insert_cart(self.user.user_id, self.cart)
        self.repository.items.insert_item(self.item)
        items = {self.item.item_id}
        for _ in range(5):
            item = self.faker.item_model
            self.repository.items.insert_item(item)
            items.add(item.item_id)
        self.repository.carts.insert_cart_items(self.cart.cart_id, items, None)
        result = self.repository.carts.select_cart_items(self.cart.cart_id)
        self.assertEqual(len(result), 6)
        self.assertIn(self.item.item_id, result)

import unittest

from api.context import Context
from api.database.repository import DatabaseRepository
from api.faker import Faker


class TestSelectCartItems(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.faker = Faker()
        self.user = self.faker.user_model
        self.repository.users.insert_user(self.user)
        self.cart = self.faker.cart_model
        self.repository.carts.insert_cart(self.user.user_id, self.cart)
        self.new_cart = self.faker.cart_model
        self.repository.carts.insert_cart(self.user.user_id, self.new_cart)
        self.item = self.faker.item_model

    def test_returns_all_cart_items(self):
        self.repository.items.insert_item(self.item)
        items = {self.item.item_id}
        for _ in range(12):
            item = self.faker.item_model
            self.repository.items.insert_item(item)
            items.add(item.item_id)
        self.repository.carts.insert_cart_items(self.cart.cart_id, items, None)
        items = set()
        for _ in range(5):
            item = self.faker.item_model
            self.repository.items.insert_item(item)
            items.add(item.item_id)
        self.repository.carts.insert_cart_items(
            self.new_cart.cart_id, items, None
        )
        result = self.repository.carts.select_cart_items(self.cart.cart_id)
        self.assertEqual(len(result), 13)
        self.assertIn(self.item.item_id, result)

    def test_returns_all_cart_items_with_origin(self):
        items = set()
        for _ in range(12):
            item = self.faker.item_model
            self.repository.items.insert_item(item)
            items.add(item.item_id)
        first_origin = self.faker.noun
        self.repository.carts.insert_cart_items(
            self.cart.cart_id, items, first_origin
        )
        items = set()
        for _ in range(5):
            item = self.faker.item_model
            self.repository.items.insert_item(item)
            items.add(item.item_id)
        second_origin = self.faker.noun
        self.repository.carts.insert_cart_items(
            self.cart.cart_id, items, second_origin
        )
        result = self.repository.carts.select_cart_items(self.cart.cart_id)
        self.assertEqual(
            len([r for r in result.values() if r.origin == first_origin]), 12
        )
        self.assertEqual(
            len([r for r in result.values() if r.origin == second_origin]), 5
        )

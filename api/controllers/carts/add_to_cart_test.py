from api.models.carts.errors import CartNotFoundError
from api.models.items.errors import ItemNotFoundError
from api.test_case import TestCase


class TestAddToCart(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.cart = self.controllers.carts.create(self.faker.cart)
        self.item = self.controllers.items.create(self.faker.item)

    def test_raises_error_if_not_found(self):
        with self.assertRaises(CartNotFoundError):
            self.controllers.carts.add_to_cart(-1, self.item.item_id)

    def test_raises_error_if_item_not_found(self):
        with self.assertRaises(ItemNotFoundError):
            self.controllers.carts.add_to_cart(self.cart.cart_id, -1)

    def test_upserts_item(self):
        for _ in range(5):
            item = self.controllers.items.create(self.faker.item)
            self.controllers.carts.add_to_cart(self.cart.cart_id, item.item_id)
        result = self.controllers.carts.add_to_cart(
            self.cart.cart_id, self.item.item_id
        )
        check = self.controllers.carts.read(self.cart.cart_id)
        self.assertEqual(result, check)

        assert result.items is not None
        self.assertEqual(len(result.items), 6)

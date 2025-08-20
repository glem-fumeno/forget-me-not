from api.models.carts.errors import CartNotFoundError
from api.test_case import TestCase


class TestReadDefault(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.cart = self.faker.cart

    def test_raises_error_if_not_found(self):
        with self.assertRaises(CartNotFoundError):
            self.controllers.carts.read_default()

    def test_returns_cart_if_found(self):
        cart = self.controllers.carts.create(self.cart)
        self.controllers.carts.update_default(cart.cart_id)
        result = self.controllers.carts.read_default()
        self.assertEqual(result.cart_id, cart.cart_id)
        self.assertEqual(result.name, cart.name)
        self.assertEqual(result.icon, cart.icon)

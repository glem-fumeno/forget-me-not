from api.models.carts.errors import CartNotFoundError
from api.test_case import TestCase


class TestDelete(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.cart = self.faker.cart

    def test_raises_error_if_not_found(self):
        with self.assertRaises(CartNotFoundError):
            self.controllers.carts.delete(-1)

    def test_found_removes_cart(self):
        cart = self.controllers.carts.create(self.cart)
        result = self.controllers.carts.delete(cart.cart_id)
        self.assertEqual(cart.cart_id, result.cart_id)
        self.assertEqual(cart.name, result.name)
        self.assertEqual(cart.icon, result.icon)
        with self.assertRaises(CartNotFoundError):
            self.controllers.carts.read(cart.cart_id)

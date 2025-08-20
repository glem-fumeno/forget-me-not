from api.models.carts.errors import CartNotFoundError
from api.models.carts.requests import CartUpdateRequest
from api.test_case import TestCase


class TestUpdate(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.cart = self.controllers.carts.create(self.faker.cart)
        self.request = CartUpdateRequest()

    def test_raises_error_if_not_found(self):
        with self.assertRaises(CartNotFoundError):
            self.controllers.carts.update(-1, self.request)

    def test_updates_name(self):
        self.request.name = self.faker.noun
        result = self.controllers.carts.update(self.cart.cart_id, self.request)
        check = self.controllers.carts.read(self.cart.cart_id)
        self.assertEqual(result, check)

        self.assertEqual(result.cart_id, self.cart.cart_id)
        self.assertEqual(result.name, self.request.name)
        self.assertEqual(result.icon, self.cart.icon)

    def test_updates_icon(self):
        self.request.icon = self.faker.icon
        result = self.controllers.carts.update(self.cart.cart_id, self.request)
        check = self.controllers.carts.read(self.cart.cart_id)
        self.assertEqual(result, check)

        self.assertEqual(result.cart_id, self.cart.cart_id)
        self.assertEqual(result.name, self.cart.name)
        self.assertEqual(result.icon, self.request.icon)

from api.test_case import TestCase


class TestCreate(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.request = self.faker.cart

    def test_new_name_creates_cart(self):
        result = self.controllers.carts.create(self.request)
        check = self.controllers.carts.read(result.cart_id)
        self.assertEqual(result, check)

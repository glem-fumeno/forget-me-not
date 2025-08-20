from api.test_case import TestCase


class TestSearch(TestCase):

    def test_returns_all_carts(self):
        for _ in range(12):
            self.controllers.carts.create(self.faker.cart)
        result = self.controllers.carts.search()
        self.assertEqual(len(result.carts), 12)
        self.assertEqual(result.count, 12)

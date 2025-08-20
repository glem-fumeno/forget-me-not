from api.test_case import TestCase


class TestSearch(TestCase):

    def test_returns_all_items(self):
        for _ in range(12):
            self.controllers.items.create(self.faker.item)
        result = self.controllers.items.search()
        self.assertEqual(len(result.items), 12)
        self.assertEqual(result.count, 12)

from api.models.items.errors import ItemExistsError
from api.test_case import TestCase


class TestCreate(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.request = self.faker.item

    def test_name_exists_raises_error(self):
        self.controllers.items.create(self.request)
        with self.assertRaises(ItemExistsError):
            self.controllers.items.create(self.request)

    def test_new_name_creates_item(self):
        result = self.controllers.items.create(self.request)
        check = self.controllers.items.read(result.item_id)
        self.assertEqual(result, check)

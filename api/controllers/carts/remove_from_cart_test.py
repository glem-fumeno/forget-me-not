import unittest

from api.context import Context
from api.controllers.controllers import Controllers
from api.controllers.mock_repository import MockRepository
from api.errors import LoggedOut
from api.faker import Faker
from api.models.carts.errors import CartNotFoundError
from api.models.items.errors import ItemNotFoundError


class TestRemoveFromCart(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = Context()
        self.faker = Faker()
        self.controllers = Controllers(self.ctx, MockRepository())
        self.login = self.faker.login
        self.user = self.controllers.users.register(self.login)
        self.ctx.add("token", self.user.token)
        self.cart = self.controllers.carts.create(self.faker.cart)
        self.item = self.controllers.items.create(self.faker.item)

    def test_raises_error_if_not_found(self):
        with self.assertRaises(CartNotFoundError):
            self.controllers.carts.remove_from_cart(-1, self.item.item_id)

    def test_raises_error_if_item_not_found(self):
        with self.assertRaises(ItemNotFoundError):
            self.controllers.carts.remove_from_cart(self.cart.cart_id, -1)

    def test_removes_item(self):
        for _ in range(5):
            item = self.controllers.items.create(self.faker.item)
            self.controllers.carts.add_to_cart(self.cart.cart_id, item.item_id)
        self.controllers.carts.add_to_cart(
            self.cart.cart_id, self.item.item_id
        )
        result = self.controllers.carts.remove_from_cart(
            self.cart.cart_id, self.item.item_id
        )
        check = self.controllers.carts.read(self.cart.cart_id)
        self.assertEqual(result, check)

        assert result.items is not None
        self.assertEqual(len(result.items), 5)

    def test_user_logged_out_raises_error(self):
        self.ctx.add("token", "")
        with self.assertRaises(LoggedOut):
            self.controllers.carts.remove_from_cart(-1, -1)

import unittest

from api.context import Context
from api.errors import Inaccessible, LoggedOut
from api.carts.controllers.core_test import CartTestRepository
from api.carts.controllers.update import CartUpdateController
from api.carts.schemas.errors import (
    CartNotFoundError,
)
from api.carts.schemas.requests import CartUpdateRequest


class TestUpdate(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = CartTestRepository()
        self.user_id = self.repository.email_map["alice.anderson@example.com"]
        self.ctx = Context().add("token", self.repository.login(self.user_id))
        self.controller = CartUpdateController(self.ctx, self.repository)

    def test_raises_error_if_not_found(self):
        request = CartUpdateRequest()
        with self.assertRaises(CartNotFoundError):
            self.controller.run(-1, request)

    def test_updates_name(self):
        request = CartUpdateRequest(name="shopping")
        cart_id = self.repository.cart_name_map[self.user_id, "groceries"]
        model = self.repository.cart_map[cart_id].copy()
        result = self.controller.run(cart_id, request)
        new_model = self.repository.cart_map[cart_id].copy()

        self.assertEqual(model.cart_id, new_model.cart_id)
        self.assertNotEqual(model.name, new_model.name)
        self.assertEqual(model.icon, new_model.icon)

        self.assertEqual(result.cart_id, cart_id)
        self.assertEqual(result.name, request.name)
        self.assertEqual(result.icon, model.icon)

    def test_updates_icon(self):
        request = CartUpdateRequest(
            icon="https://img.icons8.com/pulsar-line/96/shopping-trolley.png"
        )
        cart_id = self.repository.cart_name_map[self.user_id, "groceries"]
        model = self.repository.cart_map[cart_id].copy()
        result = self.controller.run(cart_id, request)
        new_model = self.repository.cart_map[cart_id].copy()

        self.assertEqual(model.cart_id, new_model.cart_id)
        self.assertEqual(model.name, new_model.name)
        self.assertNotEqual(model.icon, new_model.icon)

        self.assertEqual(result.cart_id, cart_id)
        self.assertEqual(result.name, model.name)
        self.assertEqual(result.icon, request.icon)

    def test_user_logged_out_raises_error(self):
        self.controller.ctx = self.controller.ctx.add("token", "")
        with self.assertRaises(LoggedOut):
            self.controller.run(-1, CartUpdateRequest())

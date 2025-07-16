import unittest

from api.context import Context
from api.controllers.carts.create import CartCreateController
from api.controllers.mock_repository import MockRepository
from api.errors import LoggedOut
from api.models.carts.requests import CartCreateRequest


class TestCreate(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = MockRepository()
        user_id = self.repository.email_map["alice.anderson@example.com"]
        self.ctx = Context().add("token", self.repository.login(user_id))
        self.controller = CartCreateController(self.ctx, self.repository)

    def test_new_name_creates_cart(self):
        result = self.controller.run(
            CartCreateRequest(
                name="office supplies",
                icon="https://img.icons8.com/pulsar-line/96/length-1.png",
            )
        )
        self.assertIn(result.cart_id, self.repository.cart_map)

    def test_user_logged_out_raises_error(self):
        self.controller.ctx = self.controller.ctx.add("token", "")
        with self.assertRaises(LoggedOut):
            self.controller.run(
                CartCreateRequest(
                    name="office supplies",
                    icon="https://img.icons8.com/pulsar-line/96/length-1.png",
                )
            )

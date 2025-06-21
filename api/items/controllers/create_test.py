import unittest

from api.context import Context
from api.errors import Inaccessible, LoggedOut
from api.items.controllers.core_test import ItemTestRepository
from api.items.controllers.create import ItemCreateController
from api.items.schemas.errors import ItemExistsError
from api.items.schemas.requests import ItemCreateRequest


class TestCreate(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = ItemTestRepository()
        user_id = self.repository.email_map["alice.anderson@example.com"]
        self.ctx = Context().add("token", self.repository.login(user_id))
        self.controller = ItemCreateController(self.ctx, self.repository)

    def test_name_exists_raises_error(self):
        with self.assertRaises(ItemExistsError):
            self.controller.run(
                ItemCreateRequest(
                    "milk",
                    "https://img.icons8.com/pulsar-line/96/milk-carton.png",
                )
            )

    def test_new_name_creates_item(self):
        self.controller.run(
            ItemCreateRequest(
                "soap", "https://img.icons8.com/pulsar-line/96/soap.png"
            )
        )
        self.assertIn("soap", self.repository.item_name_map)

    def test_user_logged_out_raises_error(self):
        self.controller.ctx = self.controller.ctx.add("token", "")
        with self.assertRaises(LoggedOut):
            self.controller.run(
                ItemCreateRequest(
                    "soap", "https://img.icons8.com/pulsar-line/96/soap.png"
                )
            )

    def test_user_role_raises_error(self):
        user_id = self.repository.email_map["bob.baker@example.com"]
        self.controller.ctx = self.controller.ctx.add(
            "token", self.repository.login(user_id)
        )
        with self.assertRaises(Inaccessible):
            self.controller.run(
                ItemCreateRequest(
                    "soap", "https://img.icons8.com/pulsar-line/96/soap.png"
                )
            )

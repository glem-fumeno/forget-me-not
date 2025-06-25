import unittest

from api.context import Context
from api.users.controllers.core_test import UserTestRepository
from api.users.controllers.register import UserRegisterController
from api.users.schemas.errors import UserExistsError
from api.users.schemas.requests import UserLoginRequest


class TestRegister(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = Context()
        self.repository = UserTestRepository()
        self.controller = UserRegisterController(self.ctx, self.repository)

    def test_register_email_exists_raises_error(self):
        with self.assertRaises(UserExistsError):
            self.controller.run(
                UserLoginRequest(
                    email="alice.anderson@example.com",
                    password="CoffeeLover#1",
                )
            )

    def test_register_new_email_creates_user(self):
        self.controller.run(
            UserLoginRequest(
                email="charlie.cooper@example.com", password="CoffeeLover#1"
            ),
        )
        self.assertIn("charlie.cooper@example.com", self.repository.email_map)

    def test_register_creates_session(self):
        response = self.controller.run(
            UserLoginRequest(
                email="charlie.cooper@example.com", password="CoffeeLover#1"
            ),
        )
        self.assertIn(response.token, self.repository.user_login_map)

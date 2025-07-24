import unittest

from api.context import Context
from api.controllers.controllers import Controllers
from api.controllers.mock_repository import MockRepository
from api.models.users.errors import InvalidCredentialsError
from api.models.users.requests import UserLoginRequest


class TestLogin(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = Context()
        self.repository = MockRepository(True)
        self.controllers = Controllers(self.ctx, self.repository)
        self.request = UserLoginRequest(
            email="alice.anderson@example.com", password="CoffeeLover#1"
        )

    def test_login_credentials_not_found_raises_error(self):
        with self.assertRaises(InvalidCredentialsError):
            self.controllers.users.login(self.request)

    def test_login_email_not_found_raises_error(self):
        self.controllers.users.register(self.request)
        self.request.email = "charlie.cooper@example.com"
        with self.assertRaises(InvalidCredentialsError):
            self.controllers.users.login(self.request)

    def test_login_password_not_found_raises_error(self):
        self.controllers.users.register(self.request)
        self.request.password = "DifferentPassword$2"
        with self.assertRaises(InvalidCredentialsError):
            self.controllers.users.login(self.request)

    def test_login_credentials_found_creates_a_new_session(self):
        response_1 = self.controllers.users.register(self.request)
        response_2 = self.controllers.users.login(self.request)
        self.assertNotEqual(response_1.token, response_2.token)
        self.controllers.ctx.add("token", response_2.token)
        self.controllers.users.read(response_2.user_id)

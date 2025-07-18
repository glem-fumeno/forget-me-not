import unittest

from api.context import Context
from api.controllers.mock_repository import MockRepository
from api.controllers.users.login import UserLoginController
from api.models.users.errors import InvalidCredentialsError
from api.models.users.requests import UserLoginRequest


class TestLogin(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = Context()
        self.repository = MockRepository()
        self.controller = UserLoginController(self.ctx, self.repository)

    def test_login_credentials_not_found_raises_error(self):
        requests = [
            UserLoginRequest(
                email="charlie.cooper@example.com", password="CoffeeLover#1"
            ),
            UserLoginRequest(
                email="alice.anderson@example.com", password="CoffeeLover#1"
            ),
            UserLoginRequest(
                email="charlie.cooper@example.com", password="SunsetDrive@34"
            ),
        ]
        for request in requests:
            with self.subTest(request=request):
                with self.assertRaises(InvalidCredentialsError):
                    self.controller.run(request)

    def test_login_credentials_found_creates_a_new_session(self):
        response_1 = self.controller.run(
            UserLoginRequest(
                email="alice.anderson@example.com", password="A1ice_89rocks"
            )
        )
        self.assertIn(response_1.token, self.repository.user_login_map)
        response_2 = self.controller.run(
            UserLoginRequest(
                email="alice.anderson@example.com", password="A1ice_89rocks"
            )
        )
        self.assertIn(response_2.token, self.repository.user_login_map)
        self.assertNotEqual(response_1.token, response_2.token)

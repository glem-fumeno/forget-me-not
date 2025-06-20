import unittest

from api.context import Context
from api.users.controllers.core_test import UserTestRepository
from api.users.controllers.login import UserLoginController
from api.users.schemas.errors import InvalidCredentialsError
from api.users.schemas.requests import UserLoginRequest


class TestLogin(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = Context()
        self.repository = UserTestRepository()
        self.controller = UserLoginController(self.ctx, self.repository)

    def test_login_credentials_not_found_raises_error(self):
        requests = [
            UserLoginRequest("charlie.cooper@example.com", "CoffeeLover#1"),
            UserLoginRequest("alice.anderson@example.com", "CoffeeLover#1"),
            UserLoginRequest("charlie.cooper@example.com", "SunsetDrive@34"),
        ]
        for request in requests:
            with self.subTest(request=request):
                with self.assertRaises(InvalidCredentialsError):
                    self.controller.run(request)

    def test_login_credentials_found_creates_a_new_session(self):
        response_1 = self.controller.run(
            UserLoginRequest("alice.anderson@example.com", "A1ice_89rocks")
        )
        self.assertIn(response_1.token, self.repository.user_login_map)
        response_2 = self.controller.run(
            UserLoginRequest("alice.anderson@example.com", "A1ice_89rocks")
        )
        self.assertIn(response_2.token, self.repository.user_login_map)
        self.assertNotEqual(response_1.token, response_2.token)

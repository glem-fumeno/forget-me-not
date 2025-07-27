import unittest

from api.context import Context
from api.controllers.controllers import Controllers
from api.controllers.mock_repository import MockRepository
from api.faker import Faker
from api.models.users.errors import InvalidCredentialsError


class TestLogin(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = Context()
        self.faker = Faker()
        self.controllers = Controllers(self.ctx, MockRepository())
        self.request = self.faker.login

    def test_login_credentials_not_found_raises_error(self):
        with self.assertRaises(InvalidCredentialsError):
            self.controllers.users.login(self.request)

    def test_login_email_not_found_raises_error(self):
        self.controllers.users.register(self.request)
        self.request.email = self.faker.email
        with self.assertRaises(InvalidCredentialsError):
            self.controllers.users.login(self.request)

    def test_login_password_not_found_raises_error(self):
        self.controllers.users.register(self.request)
        self.request.password = self.faker.password
        with self.assertRaises(InvalidCredentialsError):
            self.controllers.users.login(self.request)

    def test_login_credentials_found_creates_a_new_session(self):
        response_1 = self.controllers.users.register(self.request)
        response_2 = self.controllers.users.login(self.request)
        self.assertNotEqual(response_1.token, response_2.token)
        self.ctx.add("token", response_2.token)
        self.controllers.users.read(response_2.user_id)

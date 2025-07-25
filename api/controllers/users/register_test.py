import unittest

from api.context import Context
from api.controllers.controllers import Controllers
from api.controllers.mock_repository import MockRepository
from api.models.users.errors import UserExistsError


class TestRegister(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = Context()
        self.repository = MockRepository(True)
        self.controllers = Controllers(self.ctx, self.repository)
        self.request = self.repository.faker.login

    def test_register_does_not_change_request(self):
        request = self.request.model_copy()
        self.controllers.users.register(self.request)
        self.assertEqual(request, self.request)

    def test_register_email_exists_raises_error(self):
        self.controllers.users.register(self.request)
        with self.assertRaises(UserExistsError):
            self.controllers.users.register(self.request)

    def test_register_new_email_creates_user(self):
        credentials = self.controllers.users.register(self.request)
        self.controllers.ctx.add("token", credentials.token)
        self.controllers.users.read(credentials.user_id)

    def test_register_first_email_is_admin(self):
        result = self.controllers.users.register(self.request)
        self.assertEqual(result.role, "admin")

    def test_register_second_email_is_new(self):
        self.controllers.users.register(self.repository.faker.login)
        result = self.controllers.users.register(self.request)
        self.assertEqual(result.role, "new")

    def test_register_creates_session(self):
        response = self.controllers.users.register(self.request)
        self.assertIn(response.token, self.repository.user_login_map)

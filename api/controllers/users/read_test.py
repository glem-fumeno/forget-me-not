import unittest

from api.context import Context
from api.controllers.controllers import Controllers
from api.controllers.mock_repository import MockRepository
from api.models.users.errors import LoggedOut, UserNotFoundError


class TestRead(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = Context()
        self.repository = MockRepository(True)
        self.controllers = Controllers(self.ctx, self.repository)
        self.request = self.repository.faker.login
        self.user = self.controllers.users.register(self.request)

    def test_logged_out_raises_error(self):
        with self.assertRaises(LoggedOut):
            self.controllers.users.read(self.user.user_id)

    def test_raises_error_if_not_found(self):
        self.controllers.ctx.add("token", self.user.token)
        with self.assertRaises(UserNotFoundError):
            self.controllers.users.read(-1)

    def test_returns_user_if_found(self):
        self.controllers.ctx.add("token", self.user.token)
        result = self.controllers.users.read(self.user.user_id)
        self.assertEqual(result.user_id, self.user.user_id)
        self.assertEqual(result.email, self.user.email)
        self.assertEqual(result.username, self.user.username)

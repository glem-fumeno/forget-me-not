import unittest

from api.context import Context
from api.controllers.controllers import Controllers
from api.controllers.faker import Faker
from api.controllers.mock_repository import MockRepository
from api.models.users.errors import LoggedOut


class TestReadMe(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = Context()
        self.faker = Faker()
        self.controllers = Controllers(self.ctx, MockRepository())
        self.login = self.faker.login
        self.user = self.controllers.users.register(self.login)

    def test_logged_out_raises_error(self):
        with self.assertRaises(LoggedOut):
            self.controllers.users.read_me()

    def test_returns_user_if_found(self):
        self.ctx.add("token", self.user.token)
        result = self.controllers.users.read_me()
        self.assertEqual(result.user_id, self.user.user_id)
        self.assertEqual(result.email, self.user.email)
        self.assertEqual(result.username, self.user.username)

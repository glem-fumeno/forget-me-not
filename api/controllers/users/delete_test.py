import unittest

from api.context import Context
from api.controllers.controllers import Controllers
from api.controllers.faker import Faker
from api.controllers.mock_repository import MockRepository
from api.models.users.errors import Inaccessible, LoggedOut, UserNotFoundError


class TestDelete(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = Context()
        self.faker = Faker()
        self.controllers = Controllers(self.ctx, MockRepository())
        self.login = self.faker.login
        self.user = self.controllers.users.register(self.login)
        self.new_login = self.faker.login
        self.new_user = self.controllers.users.register(self.new_login)

    def test_raises_error_if_not_found(self):
        self.ctx.add("token", self.user.token)
        with self.assertRaises(UserNotFoundError):
            self.controllers.users.delete(-1)

    def test_found_removes_user(self):
        self.ctx.add("token", self.new_user.token)
        result = self.controllers.users.delete(self.new_user.user_id)
        self.assertEqual(self.new_user.user_id, result.user_id)
        self.assertEqual(self.new_user.email, result.email)
        self.assertEqual(self.new_user.username, result.username)
        self.ctx.add("token", self.user.token)
        with self.assertRaises(UserNotFoundError):
            self.controllers.users.read(self.new_user.user_id)

    def test_logged_out_raises_error(self):
        with self.assertRaises(LoggedOut):
            self.controllers.users.delete(self.user.user_id)

    def test_different_user_raises_error(self):
        self.ctx.add("token", self.new_user.token)
        with self.assertRaises(Inaccessible):
            self.controllers.users.delete(self.user.user_id)

    def test_admin_raises_no_error(self):
        self.ctx.add("token", self.user.token)
        self.controllers.users.delete(self.new_user.user_id)

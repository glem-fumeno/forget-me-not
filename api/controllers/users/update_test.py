import unittest

from api.context import Context
from api.controllers.controllers import Controllers
from api.controllers.mock_repository import MockRepository
from api.models.users.errors import (
    Inaccessible,
    InvalidCredentialsError,
    LoggedOut,
    UserExistsError,
    UserNotFoundError,
)
from api.models.users.requests import UserUpdateRequest


class TestUpdate(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = Context()
        self.repository = MockRepository(True)
        self.controllers = Controllers(self.ctx, self.repository)
        self.login = self.repository.faker.login
        self.user = self.controllers.users.register(self.login)
        self.new_login = self.repository.faker.login
        self.new_user = self.controllers.users.register(self.new_login)

    def test_raises_error_if_not_found(self):
        request = UserUpdateRequest()
        self.controllers.ctx.add("token", self.user.token)
        with self.assertRaises(UserNotFoundError):
            self.controllers.users.update(-1, request)

    def test_updates_email(self):
        self.controllers.ctx.add("token", self.new_user.token)
        request = UserUpdateRequest(email=self.repository.faker.email)
        result = self.controllers.users.update(self.new_user.user_id, request)
        check = self.controllers.users.read(self.new_user.user_id)

        self.assertEqual(result, check)

        self.assertEqual(self.new_user.user_id, result.user_id)
        self.assertEqual(self.new_user.username, result.username)
        self.assertEqual(request.email, result.email)

    def test_raises_error_if_email_taken(self):
        self.controllers.ctx.add("token", self.new_user.token)
        request = UserUpdateRequest(email=self.user.email)
        with self.assertRaises(UserExistsError):
            self.controllers.users.update(self.new_user.user_id, request)

    def test_raises_no_error_if_email_taken_is_self(self):
        self.controllers.ctx.add("token", self.new_user.token)
        request = UserUpdateRequest(email=self.new_user.email)
        self.controllers.users.update(self.new_user.user_id, request)

    def test_updates_username(self):
        self.controllers.ctx.add("token", self.new_user.token)
        request = UserUpdateRequest(username=self.repository.faker.username)
        result = self.controllers.users.update(self.new_user.user_id, request)
        check = self.controllers.users.read(self.new_user.user_id)

        self.assertEqual(result, check)

        self.assertEqual(self.new_user.user_id, result.user_id)
        self.assertEqual(request.username, result.username)
        self.assertEqual(self.new_user.email, result.email)

    def test_updates_password(self):
        self.controllers.ctx.add("token", self.new_user.token)
        password = self.repository.faker.password
        request = UserUpdateRequest(password=password)
        self.controllers.users.update(self.new_user.user_id, request)
        with self.assertRaises(InvalidCredentialsError):
            self.controllers.users.login(self.new_login)
        self.new_login.password = password
        self.controllers.users.login(self.new_login)

    def test_logged_out_raises_error(self):
        request = UserUpdateRequest()
        with self.assertRaises(LoggedOut):
            self.controllers.users.update(self.new_user.user_id, request)

    def test_different_user_raises_error(self):
        self.controllers.ctx.add("token", self.new_user.token)
        request = UserUpdateRequest()
        with self.assertRaises(Inaccessible):
            self.controllers.users.update(self.user.user_id, request)

    def test_admin_raises_no_error(self):
        self.controllers.ctx.add("token", self.user.token)
        request = UserUpdateRequest()
        self.controllers.users.update(self.new_user.user_id, request)

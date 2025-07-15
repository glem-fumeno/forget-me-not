import unittest

from api.context import Context
from api.controllers.users.core_test import UserTestRepository
from api.controllers.users.delete import UserDeleteController
from api.models.users.errors import Inaccessible, LoggedOut, UserNotFoundError


class TestDelete(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = UserTestRepository()
        user_id = self.repository.email_map["alice.anderson@example.com"]
        self.ctx = Context().add("token", self.repository.login(user_id))
        self.controller = UserDeleteController(self.ctx, self.repository)

    def test_raises_error_if_not_found(self):
        with self.assertRaises(UserNotFoundError):
            self.controller.run(-1)

    def test_found_removes_user(self):
        user_id = self.repository.email_map["alice.anderson@example.com"]
        user = self.repository.user_map[user_id]
        result = self.controller.run(user_id)
        self.assertNotIn(user_id, self.repository.user_map)
        self.assertEqual(user.user_id, result.user_id)
        self.assertEqual(user.email, result.email)
        self.assertEqual(user.username, result.username)

    def test_logged_out_raises_error(self):
        user_id = self.repository.email_map["alice.anderson@example.com"]
        self.controller.ctx = self.controller.ctx.add("token", "")

        with self.assertRaises(LoggedOut):
            self.controller.run(user_id)

    def test_different_user_raises_error(self):
        user_id = self.repository.email_map["alice.anderson@example.com"]
        requestee_id = self.repository.email_map["bob.baker@example.com"]
        self.controller.ctx = self.controller.ctx.add(
            "token", self.repository.login(requestee_id)
        )

        with self.assertRaises(Inaccessible):
            self.controller.run(user_id)

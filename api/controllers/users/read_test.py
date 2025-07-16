import unittest

from api.context import Context
from api.controllers.mock_repository import MockRepository
from api.controllers.users.read import UserReadController
from api.models.users.errors import LoggedOut, UserNotFoundError


class TestRead(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = MockRepository()
        user_id = self.repository.email_map["alice.anderson@example.com"]
        self.ctx = Context().add("token", self.repository.login(user_id))
        self.controller = UserReadController(self.ctx, self.repository)

    def test_raises_error_if_not_found(self):
        with self.assertRaises(UserNotFoundError):
            self.controller.run(-1)

    def test_returns_user_if_found(self):
        user_id = self.repository.email_map["alice.anderson@example.com"]
        model = self.repository.user_map[user_id]
        result = self.controller.run(user_id)
        self.assertEqual(result.user_id, user_id)
        self.assertEqual(result.email, model.email)
        self.assertEqual(result.username, model.username)

    def test_logged_out_raises_error(self):
        user_id = self.repository.email_map["alice.anderson@example.com"]
        self.controller.ctx = self.controller.ctx.add("token", "")

        with self.assertRaises(LoggedOut):
            self.controller.run(user_id)

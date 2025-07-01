import unittest

from api.context import Context
from api.users.controllers.core_test import UserTestRepository
from api.users.controllers.read_me import UserReadMeController
from api.users.schemas.errors import LoggedOut


class TestReadMe(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = UserTestRepository()
        user_id = self.repository.email_map["alice.anderson@example.com"]
        self.ctx = Context().add("token", self.repository.login(user_id))
        self.controller = UserReadMeController(self.ctx, self.repository)

    def test_returns_user_if_found(self):
        user_id = self.repository.email_map["alice.anderson@example.com"]
        model = self.repository.user_map[user_id]
        result = self.controller.run()
        self.assertEqual(result.user_id, user_id)
        self.assertEqual(result.email, model.email)
        self.assertEqual(result.username, model.username)

    def test_logged_out_raises_error(self):
        self.controller.ctx = self.controller.ctx.add("token", "")

        with self.assertRaises(LoggedOut):
            self.controller.run()

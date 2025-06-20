import unittest

from api.context import Context
from api.users.controllers.core_test import UserTestRepository
from api.users.controllers.delete import UserDeleteController
from api.users.schemas.errors import UserNotFoundError


class TestDelete(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = Context()
        self.repository = UserTestRepository()
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

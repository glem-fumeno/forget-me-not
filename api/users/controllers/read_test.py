import unittest

from api.users.controllers.core_test import UserTestRepository
from api.users.controllers.read import UserReadController
from api.users.schemas.errors import UserNotFoundError


class TestRead(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = UserTestRepository()
        self.controller = UserReadController(self.repository)

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

import unittest

from api.context import Context
from api.database.test_repository import DatabaseTestRepository


class TestSelectUser(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseTestRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.repository.initialize_test_cases()

    def test_returns_none_when_no_user(self):
        result = self.repository.users.select_user(-1)
        self.assertIsNone(result)

    def test_returns_user_when_found(self):
        user_id = self.repository.email_map["alice.anderson@example.com"]
        result = self.repository.users.select_user(user_id)
        self.assertEqual(result, self.repository.user_map[user_id])

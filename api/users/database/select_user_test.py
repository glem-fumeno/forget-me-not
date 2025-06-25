import unittest

from api.context import Context
from api.users.database.core_test import UserDatabaseTestRepository


class TestSelectUser(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = UserDatabaseTestRepository(Context(), "test.db")
        self.repository.connect()
        self.repository.initialize_test_cases()

    def tearDown(self) -> None:
        self.repository.connection.rollback()
        self.repository.connection.close()

    def test_returns_none_when_no_user(self):
        result = self.repository.select_user(-1)
        self.assertIsNone(result)

    def test_returns_user_when_found(self):
        user_id = self.repository.email_map["alice.anderson@example.com"]
        result = self.repository.select_user(user_id)
        self.assertEqual(result, self.repository.user_map[user_id])

import unittest

from api.context import Context
from api.database.test_repository import DatabaseTestRepository


class TestSelectUsers(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseTestRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.repository.initialize_test_cases()

    def test_returns(self):
        result = self.repository.select_users()
        self.assertEqual(len(result), 2)
        self.assertIn(
            self.repository.email_map["alice.anderson@example.com"], result
        )
        self.assertIn(
            self.repository.email_map["bob.baker@example.com"], result
        )

import unittest

from api.context import Context
from api.users.database.core_test import UserDatabaseTestRepository


class TestSelectUsers(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = UserDatabaseTestRepository(Context(), "test.db")
        self.repository.connect()
        self.repository.initialize_test_cases()

    def tearDown(self) -> None:
        self.repository.connection.rollback()
        self.repository.connection.close()

    def test_returns(self):
        result = self.repository.select_users()
        self.assertEqual(len(result), 2)
        self.assertIn(
            self.repository.email_map["alice.anderson@example.com"], result
        )
        self.assertIn(
            self.repository.email_map["bob.baker@example.com"], result
        )

import unittest

from api.context import Context
from api.database.test_repository import DatabaseTestRepository


class TestDeleteUser(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseTestRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.repository.initialize_test_cases()

    def test_returns_user_when_found(self):
        user_id = self.repository.email_map["alice.anderson@example.com"]
        self.repository.users.delete_user(user_id)
        result = self.repository.cursor.execute(
            """
            SELECT user_id_ FROM users_ WHERE user_id_ = ?
            """,
            (user_id,),
        )
        self.assertIsNone(result.fetchone())

import unittest

from api.context import Context
from api.users.database.core_test import UserDatabaseTestRepository


class TestDeleteUser(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = UserDatabaseTestRepository(Context(), "test.db")
        self.repository.connect()
        self.repository.initialize_test_cases()

    def tearDown(self) -> None:
        self.repository.connection.rollback()
        self.repository.connection.close()

    def test_returns_user_when_found(self):
        user_id = self.repository.email_map["alice.anderson@example.com"]
        self.repository.delete_user(user_id)
        result = self.repository.cursor.execute(
            """
            SELECT user_id_ FROM users_ WHERE user_id_ = ?
            """,
            (user_id,),
        )
        self.assertIsNone(result.fetchone())

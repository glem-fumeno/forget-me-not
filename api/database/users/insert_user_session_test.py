import unittest

from api.context import Context
from api.database.test_repository import DatabaseTestRepository
from api.models.users.models import UserSessionModel
from api.security import get_uuid


class TestInsertUserSession(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseTestRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.repository.initialize_test_cases()

    def test_inserts_user_session_to_db(self):
        user_id = self.repository.email_map["bob.baker@example.com"]
        model = UserSessionModel(user_id=user_id, token=get_uuid())
        self.repository.insert_user_session(model)
        result = self.repository.cursor.execute(
            """
            SELECT user_id_ FROM users_sessions_ WHERE token_ = ?
            """,
            (model.token,),
        )
        self.assertEqual(model.user_id, result.fetchone()[0])

import unittest

from api.context import Context
from api.security import get_uuid
from api.database.users.core_test import UserDatabaseTestRepository
from api.models.users.models import UserSessionModel


class TestInsertUserSession(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = UserDatabaseTestRepository(Context(), "test.db")
        self.repository.connect()
        self.repository.initialize_test_cases()

    def tearDown(self) -> None:
        self.repository.connection.rollback()
        self.repository.connection.close()

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

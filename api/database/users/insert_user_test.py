import unittest

from api.context import Context
from api.database.test_repository import DatabaseTestRepository
from api.models.users.models import UserModel


class TestInsertUser(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseTestRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.repository.initialize_test_cases()

    def test_changes_user_id(self):
        model = UserModel(
            user_id=-1,
            username="copperc",
            email="charlie.cooper@example.com",
            password="CoffeeLover#1",
            role="new",
        )
        self.repository.insert_user(model)
        self.assertNotEqual(model.user_id, -1)

    def test_inserts_user_to_db(self):
        model = UserModel(
            user_id=-1,
            username="copperc",
            email="charlie.cooper@example.com",
            password="CoffeeLover#1",
            role="new",
        )
        self.repository.insert_user(model)
        result = self.repository.cursor.execute(
            """
            SELECT user_id_ FROM users_ WHERE user_id_ = ?
            """,
            (model.user_id,),
        )
        self.assertEqual(model.user_id, result.fetchone()[0])

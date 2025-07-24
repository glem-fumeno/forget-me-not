import unittest

from api.context import Context
from api.database.test_repository import DatabaseTestRepository
from api.models.users.models import UserModel
from api.security import get_hash


class TestUpdateUser(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseTestRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.repository.initialize_test_cases()

    def test_updates_user_in_db(self):
        user_id = self.repository.email_map["bob.baker@example.com"]
        model = UserModel(
            user_id=user_id,
            username="copperc",
            email="charlie.cooper@example.com",
            password=get_hash("CoffeeLover#1"),
            role="new",
        )
        self.repository.users.update_user(model)
        result = self.repository.cursor.execute(
            """
            SELECT user_id_, username_, email_, password_, role_
            FROM users_
            WHERE user_id_ = ?
            """,
            (user_id,),
        )
        new_model = UserModel.from_db(result.description, result.fetchone())
        self.assertEqual(model, new_model)

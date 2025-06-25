import unittest

from api.users.common import get_hash
from api.users.database.core_test import UserDatabaseTestRepository
from api.users.schemas.models import UserModel


class TestUpdateUser(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = UserDatabaseTestRepository("test.db")
        self.repository.connect()
        self.repository.initialize_test_cases()

    def tearDown(self) -> None:
        self.repository.connection.rollback()
        self.repository.connection.close()

    def test_updates_user_in_db(self):
        user_id = self.repository.email_map["bob.baker@example.com"]
        model = UserModel(
            user_id=user_id,
            username="copperc",
            email="charlie.cooper@example.com",
            password=get_hash("CoffeeLover#1"),
            role="new",
        )
        self.repository.update_user(model)
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

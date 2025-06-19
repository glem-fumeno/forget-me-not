import unittest

from api.users.database.core_test import UserDatabaseTestRepository
from api.users.schemas.models import UserModel


class TestInsertUser(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = UserDatabaseTestRepository("test.db").__enter__()
        self.repository.connect()
        self.repository.initialize_test_cases()

    def tearDown(self) -> None:
        self.repository.connection.rollback()
        self.repository.connection.close()

    def test_insert_user_changes_user_id(self):
        model = UserModel(
            -1, "copperc", "charlie.cooper@example.com", "CoffeeLover#1"
        )
        self.repository.insert_user(model)
        self.assertNotEqual(model.user_id, -1)

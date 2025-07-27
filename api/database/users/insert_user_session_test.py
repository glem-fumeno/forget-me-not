import unittest

from api.context import Context
from api.database.repository import DatabaseRepository
from api.faker import Faker
from api.security import get_uuid


class TestInsertUserSession(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseRepository(Context(), ":memory:")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.faker = Faker()
        self.model = self.faker.user_model

    def test_inserts_user_session_to_db(self):
        self.repository.users.insert_user(self.model)
        token = get_uuid()
        self.repository.users.insert_user_session(self.model.user_id, token)
        result = self.repository.users.select_user_by_token(token)
        self.assertIsNotNone(result)

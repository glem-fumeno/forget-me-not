import unittest

from api.context import Context
from api.database.repository import DatabaseRepository
from api.faker import Faker
from api.security import get_uuid


class TestSelectUserByToken(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseRepository(Context(), ":memory:")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.faker = Faker()
        self.model = self.faker.user_model

    def test_returns_none_when_no_user(self):
        result = self.repository.users.select_user_by_token("")
        self.assertIsNone(result)

    def test_returns_user_when_found(self):
        self.repository.users.insert_user(self.model)
        token = get_uuid()
        self.repository.users.insert_user_session(self.model.user_id, token)
        result = self.repository.users.select_user_by_token(token)
        self.assertEqual(result, self.model)

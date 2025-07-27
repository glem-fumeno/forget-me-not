import unittest

from api.context import Context
from api.database.repository import DatabaseRepository
from api.faker import Faker


class TestSelectUser(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.faker = Faker()
        self.model = self.faker.user_model

    def test_returns_none_when_no_user(self):
        result = self.repository.users.select_user(-1)
        self.assertIsNone(result)

    def test_returns_user_when_found(self):
        self.repository.users.insert_user(self.model)
        result = self.repository.users.select_user(self.model.user_id)
        self.assertEqual(result, self.model)

import unittest

from api.context import Context
from api.database.repository import DatabaseRepository
from api.faker import Faker


class TestSelectUsers(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.faker = Faker()
        self.model = self.faker.user_model

    def test_returns(self):
        self.repository.users.insert_user(self.model)
        for _ in range(12):
            self.repository.users.insert_user(self.faker.user_model)
        result = self.repository.users.select_users()
        self.assertEqual(len(result), 13)
        self.assertEqual(self.model, result[self.model.user_id])

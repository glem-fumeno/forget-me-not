import unittest

from api.context import Context
from api.database.repository import DatabaseRepository
from api.faker import Faker


class TestSelectUserByEmail(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseRepository(Context(), ":memory:")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.faker = Faker()
        self.model = self.faker.user_model

    def test_returns_none_when_no_user(self):
        result = self.repository.users.select_user_id_by_email(
            self.faker.email
        )
        self.assertIsNone(result)

    def test_returns_user_when_found(self):
        self.repository.users.insert_user(self.model)
        result = self.repository.users.select_user_id_by_email(
            self.model.email
        )
        self.assertEqual(result, self.model.user_id)

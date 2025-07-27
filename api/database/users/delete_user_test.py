import unittest

from api.context import Context
from api.database.repository import DatabaseRepository
from api.faker import Faker


class TestDeleteUser(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.faker = Faker()
        self.model = self.faker.user_model

    def test_deletes_user_when_found(self):
        self.repository.users.insert_user(self.model)
        self.repository.users.delete_user(self.model.user_id)
        result = self.repository.users.select_user(self.model.user_id)
        self.assertIsNone(result)

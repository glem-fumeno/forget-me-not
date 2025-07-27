import unittest

from api.context import Context
from api.database.repository import DatabaseRepository
from api.faker import Faker


class TestInsertUser(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseRepository(Context(), ":memory:")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.faker = Faker()
        self.model = self.faker.user_model

    def test_changes_user_id(self):
        self.repository.users.insert_user(self.model)
        self.assertNotEqual(self.model.user_id, -1)

    def test_inserts_user_to_db(self):
        self.repository.users.insert_user(self.model)
        result = self.repository.users.select_user(self.model.user_id)
        self.assertEqual(self.model, result)

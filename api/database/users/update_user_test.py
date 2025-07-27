import unittest

from api.context import Context
from api.database.repository import DatabaseRepository
from api.faker import Faker


class TestUpdateUser(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseRepository(Context(), ":memory:")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.faker = Faker()
        self.model = self.faker.user_model

    def test_updates_user_in_db(self):
        self.repository.users.insert_user(self.model)
        model = self.faker.user_model
        model.user_id = self.model.user_id
        self.repository.users.update_user(model)
        result = self.repository.users.select_user(model.user_id)
        self.assertEqual(model, result)

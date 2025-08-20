import unittest

from api.context import Context
from api.controllers.controllers import Controllers
from api.database.repository import DatabaseRepository
from api.faker import Faker


class TestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = Context()
        self.faker = Faker()
        self.repository = DatabaseRepository(self.ctx, ":memory:")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.controllers = Controllers(self.ctx, self.repository)

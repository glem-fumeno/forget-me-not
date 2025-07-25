import unittest

from api.context import Context
from api.controllers.controllers import Controllers
from api.controllers.mock_repository import MockRepository
from api.errors import LoggedOut


class TestCreate(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = Context()
        self.repository = MockRepository(True)
        self.controllers = Controllers(self.ctx, self.repository)
        self.login = self.repository.faker.login
        self.user = self.controllers.users.register(self.login)
        self.request = self.repository.faker.recipe

    def test_new_name_creates_recipe(self):
        self.controllers.ctx.add("token", self.user.token)
        result = self.controllers.recipes.create(self.request)
        check = self.controllers.recipes.read(result.recipe_id)
        self.assertEqual(result, check)

    def test_user_logged_out_raises_error(self):
        with self.assertRaises(LoggedOut):
            self.controllers.recipes.create(self.request)

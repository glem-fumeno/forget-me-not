import unittest

from api.context import Context
from api.controllers.mock_repository import MockRepository
from api.controllers.recipes.update import RecipeUpdateController
from api.errors import LoggedOut
from api.models.recipes.errors import RecipeNotFoundError
from api.models.recipes.requests import RecipeUpdateRequest


class TestUpdate(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = MockRepository()
        self.user_id = self.repository.email_map["alice.anderson@example.com"]
        self.ctx = Context().add("token", self.repository.login(self.user_id))
        self.controller = RecipeUpdateController(self.ctx, self.repository)

    def test_raises_error_if_not_found(self):
        request = RecipeUpdateRequest()
        with self.assertRaises(RecipeNotFoundError):
            self.controller.run(-1, request)

    def test_updates_name(self):
        request = RecipeUpdateRequest(name="pancake stack")
        recipe_id = self.repository.recipe_name_map[self.user_id, "pancakes"]
        model = self.repository.recipe_map[recipe_id].copy()
        result = self.controller.run(recipe_id, request)
        new_model = self.repository.recipe_map[recipe_id].copy()

        self.assertEqual(model.recipe_id, new_model.recipe_id)
        self.assertNotEqual(model.name, new_model.name)
        self.assertEqual(model.icon, new_model.icon)

        self.assertEqual(result.recipe_id, recipe_id)
        self.assertEqual(result.name, request.name)
        self.assertEqual(result.icon, model.icon)

    def test_updates_icon(self):
        request = RecipeUpdateRequest(
            icon="https://img.icons8.com/pulsar-line/96/american-pancakes.png"
        )
        recipe_id = self.repository.recipe_name_map[self.user_id, "pancakes"]
        model = self.repository.recipe_map[recipe_id].copy()
        result = self.controller.run(recipe_id, request)
        new_model = self.repository.recipe_map[recipe_id].copy()

        self.assertEqual(model.recipe_id, new_model.recipe_id)
        self.assertEqual(model.name, new_model.name)
        self.assertNotEqual(model.icon, new_model.icon)

        self.assertEqual(result.recipe_id, recipe_id)
        self.assertEqual(result.name, model.name)
        self.assertEqual(result.icon, request.icon)

    def test_user_logged_out_raises_error(self):
        self.controller.ctx = self.controller.ctx.add("token", "")
        with self.assertRaises(LoggedOut):
            self.controller.run(-1, RecipeUpdateRequest())

import unittest

from api.context import Context
from api.users.controllers.core_test import UserTestRepository
from api.users.controllers.update import UserUpdateController
from api.users.schemas.errors import UserExistsError, UserNotFoundError
from api.users.schemas.requests import UserUpdateRequest


class TestUpdate(unittest.TestCase):
    def setUp(self) -> None:
        self.ctx = Context()
        self.repository = UserTestRepository()
        self.controller = UserUpdateController(self.ctx, self.repository)

    def test_raises_error_if_not_found(self):
        request = UserUpdateRequest()
        with self.assertRaises(UserNotFoundError):
            self.controller.run(-1, request)

    def test_updates_email(self):
        request = UserUpdateRequest(email="alice.adams@example.com")
        user_id = self.repository.email_map["alice.anderson@example.com"]
        model = self.repository.user_map[user_id].copy()
        result = self.controller.run(user_id, request)
        new_model = self.repository.user_map[user_id].copy()

        self.assertEqual(model.user_id, new_model.user_id)
        self.assertEqual(model.username, new_model.username)
        self.assertNotEqual(model.email, new_model.email)
        self.assertEqual(model.password, new_model.password)

        self.assertEqual(result.user_id, user_id)
        self.assertEqual(result.email, request.email)
        self.assertEqual(result.username, model.username)

    def test_raises_error_if_email_taken(self):
        request = UserUpdateRequest(email="bob.baker@example.com")
        user_id = self.repository.email_map["alice.anderson@example.com"]
        with self.assertRaises(UserExistsError):
            self.controller.run(user_id, request)

    def test_raises_no_error_if_email_taken_is_self(self):
        request = UserUpdateRequest(email="alice.anderson@example.com")
        user_id = self.repository.email_map["alice.anderson@example.com"]
        self.controller.run(user_id, request)

    def test_updates_username(self):
        request = UserUpdateRequest(username="alanderson")
        user_id = self.repository.email_map["alice.anderson@example.com"]
        model = self.repository.user_map[user_id].copy()
        result = self.controller.run(user_id, request)
        new_model = self.repository.user_map[user_id].copy()

        self.assertEqual(model.user_id, new_model.user_id)
        self.assertNotEqual(model.username, new_model.username)
        self.assertEqual(model.email, new_model.email)
        self.assertEqual(model.password, new_model.password)

        self.assertEqual(result.user_id, user_id)
        self.assertEqual(result.email, model.email)
        self.assertEqual(result.username, request.username)

    def test_updates_password(self):
        request = UserUpdateRequest(password="Cupcake$AreT4sty")
        user_id = self.repository.email_map["alice.anderson@example.com"]
        model = self.repository.user_map[user_id].copy()
        result = self.controller.run(user_id, request)
        new_model = self.repository.user_map[user_id].copy()

        self.assertEqual(model.user_id, new_model.user_id)
        self.assertEqual(model.username, new_model.username)
        self.assertEqual(model.email, new_model.email)
        self.assertNotEqual(model.password, new_model.password)

        self.assertEqual(result.user_id, user_id)
        self.assertEqual(result.email, model.email)
        self.assertEqual(result.username, model.username)

import unittest

from api.context import Context
from api.database.test_repository import DatabaseTestRepository
from api.models.items.models import ItemUserModel


class TestInsertItemUser(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseTestRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.repository.initialize_test_cases()

    def test_inserts_item_session_to_db(self):
        user_id = self.repository.email_map["bob.baker@example.com"]
        item_id = self.repository.item_name_map["milk"]
        model = ItemUserModel(item_id=item_id, user_id=user_id)
        self.repository.items.insert_item_user(model)
        result = self.repository.cursor.execute(
            """
            SELECT item_id_
            FROM items_users_
            WHERE user_id_ = ? AND item_id_ = ?
            """,
            (model.user_id, model.item_id),
        )
        self.assertEqual(model.item_id, result.fetchone()[0])

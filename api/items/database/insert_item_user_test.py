import unittest

from api.items.database.core_test import ItemDatabaseTestRepository
from api.items.schemas.models import ItemUserModel


class TestInsertItemUser(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = ItemDatabaseTestRepository("test.db")
        self.repository.connect()
        self.repository.initialize_test_cases()

    def tearDown(self) -> None:
        self.repository.connection.rollback()
        self.repository.connection.close()

    def test_inserts_item_session_to_db(self):
        user_id = self.repository.email_map["bob.baker@example.com"]
        item_id = self.repository.item_name_map["milk"]
        model = ItemUserModel(item_id=item_id, user_id=user_id)
        self.repository.insert_item_user(model)
        result = self.repository.cursor.execute(
            """
            SELECT item_id_
            FROM items_users_
            WHERE user_id_ = ? AND item_id_ = ?
            """,
            (model.user_id, model.item_id),
        )
        self.assertEqual(model.item_id, result.fetchone()[0])

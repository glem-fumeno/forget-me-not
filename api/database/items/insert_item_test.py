import unittest

from api.context import Context
from api.database.test_repository import DatabaseTestRepository
from api.models.items.models import ItemModel


class TestInsertItem(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = DatabaseTestRepository(Context(), "test.db")
        self.repository.__enter__()
        self.addCleanup(self.repository.__exit__, 1, None, None)
        self.repository.initialize_test_cases()

    def test_changes_item_id(self):
        model = ItemModel(
            item_id=-1,
            name="needle",
            icon="https://img.icons8.com/pulsar-line/96/needle.png",
        )
        self.repository.items.insert_item(model)
        self.assertNotEqual(model.item_id, -1)

    def test_inserts_item_to_db(self):
        model = ItemModel(
            item_id=-1,
            name="needle",
            icon="https://img.icons8.com/pulsar-line/96/needle.png",
        )
        self.repository.items.insert_item(model)
        result = self.repository.cursor.execute(
            """
            SELECT item_id_ FROM items_ WHERE item_id_ = ?
            """,
            (model.item_id,),
        )
        self.assertEqual(model.item_id, result.fetchone()[0])

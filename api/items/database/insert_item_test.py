import unittest

from api.items.database.core_test import ItemDatabaseTestRepository
from api.items.schemas.models import ItemModel


class TestInsertItem(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = ItemDatabaseTestRepository("test.db")
        self.repository.connect()
        self.repository.initialize_test_cases()

    def tearDown(self) -> None:
        self.repository.connection.rollback()
        self.repository.connection.close()

    def test_changes_item_id(self):
        model = ItemModel(
            -1, "soap", "https://img.icons8.com/pulsar-line/96/soap.png"
        )
        self.repository.insert_item(model)
        self.assertNotEqual(model.item_id, -1)

    def test_inserts_item_to_db(self):
        model = ItemModel(
            -1, "soap", "https://img.icons8.com/pulsar-line/96/soap.png"
        )
        self.repository.insert_item(model)
        result = self.repository.cursor.execute(
            """
            SELECT item_id_ FROM items_ WHERE item_id_ = ?
            """,
            (model.item_id,),
        )
        self.assertEqual(model.item_id, result.fetchone()[0])

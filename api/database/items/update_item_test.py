import unittest

from api.context import Context
from api.database.items.core_test import ItemDatabaseTestRepository
from api.models.items.models import ItemModel


class TestUpdateItem(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = ItemDatabaseTestRepository(Context(), "test.db")
        self.repository.connect()
        self.repository.initialize_test_cases()

    def tearDown(self) -> None:
        self.repository.connection.rollback()
        self.repository.connection.close()

    def test_updates_item_in_db(self):
        item_id = self.repository.item_name_map["milk"]
        model = ItemModel(
            item_id=item_id,
            name="milk carton",
            icon="https://img.icons8.com/pulsar-line/96/milk-carton.png",
        )
        self.repository.update_item(model)
        result = self.repository.cursor.execute(
            """
            SELECT item_id_, name_, icon_ FROM items_ WHERE item_id_ = ?
            """,
            (item_id,),
        )
        new_model = ItemModel.from_db(result.description, result.fetchone())
        self.assertEqual(model, new_model)

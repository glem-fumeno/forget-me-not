from api.database.operation import DatabaseOperation
from api.items.schemas.models import ItemModel


class ItemSelectItemOperation(DatabaseOperation):
    def run(self, item_id: int) -> ItemModel | None:
        result = self.cursor.execute(self.query, (item_id,))
        columns = result.fetchone()
        if columns is None:
            return
        return ItemModel.from_db(result.description, columns)

    @property
    def query(self) -> str:
        return """
            SELECT item_id_, name_, icon_
            FROM items_
            WHERE item_id_ = ?
        """

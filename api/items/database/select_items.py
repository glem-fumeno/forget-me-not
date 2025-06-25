from api.database.operation import DatabaseOperation
from api.items.schemas.models import ItemModel


class ItemSelectItemsOperation(DatabaseOperation):
    def run(self) -> dict[int, ItemModel]:
        result = self.cursor.execute(self.query)
        results = result.fetchall()
        return {
            columns[0]: ItemModel.from_db(result.description, columns)
            for columns in results
        }

    @property
    def query(self) -> str:
        return """
            SELECT item_id_, name_, icon_
            FROM items_
        """

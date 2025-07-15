from api.database.operation import DatabaseOperation
from api.models.items.models import ItemModel


class CartSelectCartItemsOperation(DatabaseOperation):
    def run(self, cart_id: int) -> list[ItemModel]:
        result = self.cursor.execute(self.query, (cart_id,))
        results = result.fetchall()
        return [
            ItemModel.from_db(result.description, columns)
            for columns in results
        ]

    @property
    def query(self) -> str:
        return """
            SELECT item_id_, name_, icon_
            FROM items_
            INNER JOIN carts_items_ USING (item_id_)
            WHERE cart_id_ = ?
            ORDER BY name_
        """

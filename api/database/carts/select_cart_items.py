from api.database.operation import DatabaseOperation
from api.models.carts.models import CartItemModel


class CartSelectCartItemsOperation(DatabaseOperation):
    def run(self, cart_id: int) -> dict[int, CartItemModel]:
        result = self.cursor.execute(self.query, (cart_id,))
        results = result.fetchall()
        return {
            columns[0]: CartItemModel.from_db(result.description, columns)
            for columns in results
        }

    @property
    def query(self) -> str:
        return """
            SELECT item_id_, origin_
            FROM carts_items_
            WHERE cart_id_ = ?
        """

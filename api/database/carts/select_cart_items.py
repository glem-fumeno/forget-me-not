from api.database.operation import DatabaseOperation


class CartSelectCartItemsOperation(DatabaseOperation):
    def run(self, cart_id: int) -> set[int]:
        result = self.cursor.execute(self.query, (cart_id,))
        return {columns[0] for columns in result.fetchall()}

    @property
    def query(self) -> str:
        return """
            SELECT item_id_
            FROM carts_items_
            WHERE cart_id_ = ?
        """

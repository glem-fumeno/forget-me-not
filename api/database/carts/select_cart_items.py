from api.database.operation import DatabaseOperation


class CartSelectCartItemsOperation(DatabaseOperation):
    def run(self, cart_id: int) -> set[tuple[int, str]]:
        result = self.cursor.execute(self.query, (cart_id,))
        results = result.fetchall()
        return {(columns[0], columns[1]) for columns in results}

    @property
    def query(self) -> str:
        return """
            SELECT item_id_, origin_
            FROM carts_items_
            WHERE cart_id_ = ?
        """

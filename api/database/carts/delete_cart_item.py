from api.database.operation import DatabaseOperation


class CartDeleteCartItemOperation(DatabaseOperation):
    def run(self, cart_id: int, item_id: int):
        self.cursor.execute(self.query, (cart_id, item_id))

    @property
    def query(self) -> str:
        return """
            DELETE FROM carts_items_ WHERE cart_id_ = ? AND item_id_ = ?
        """

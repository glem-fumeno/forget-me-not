from api.database.operation import DatabaseOperation


class CartInsertCartItemOperation(DatabaseOperation):
    def run(self, cart_id: int, item_id: int):
        self.cursor.execute(self.query, (cart_id, item_id))

    @property
    def query(self) -> str:
        return """
            INSERT INTO carts_items_ (cart_id_, item_id_)
            VALUES (?, ?)
        """

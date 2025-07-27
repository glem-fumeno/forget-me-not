from api.database.operation import DatabaseOperation


class CartInsertCartItemsOperation(DatabaseOperation):
    def run(self, cart_id: int, item_ids: set[int], origin: str):
        self.cursor.executemany(
            self.query, [(cart_id, item_id, origin) for item_id in item_ids]
        )

    @property
    def query(self) -> str:
        return """
            INSERT INTO carts_items_ (cart_id_, item_id_, origin_)
            VALUES (?, ?, ?)
        """

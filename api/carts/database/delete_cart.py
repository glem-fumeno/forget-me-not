from api.database.operation import DatabaseOperation


class CartDeleteCartOperation(DatabaseOperation):
    def run(self, cart_id: int):
        self.cursor.execute(self.query, (cart_id,))

    @property
    def query(self) -> str:
        return """
            DELETE FROM carts_ WHERE cart_id_ = ?
        """

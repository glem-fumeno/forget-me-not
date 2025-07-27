from api.database.operation import DatabaseOperation


class CartDeleteCartUserOperation(DatabaseOperation):
    def run(self, cart_id: int, user_id: int):
        self.cursor.execute(self.query, (cart_id, user_id))

    @property
    def query(self) -> str:
        return """
            DELETE FROM carts_users_ WHERE cart_id_ = ? AND user_id_ = ?
        """

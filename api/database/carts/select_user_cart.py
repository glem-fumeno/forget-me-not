from api.database.operation import DatabaseOperation


class CartSelectUserCartOperation(DatabaseOperation):
    def run(self, user_id: int) -> int | None:
        cur = self.cursor.execute(self.query, (user_id,))
        cart_id = cur.fetchone()
        if cart_id is None:
            return
        return cart_id[0]

    @property
    def query(self) -> str:
        return """
            SELECT cart_id_ FROM users_ WHERE user_id_ = ?
        """

from api.database.operation import DatabaseOperation


class CartUpdateUserCartOperation(DatabaseOperation):
    def run(self, user_id: int, cart_id: int):
        self.cursor.execute(self.query, (cart_id, user_id))

    @property
    def query(self) -> str:
        return """
            UPDATE users_
            SET cart_id_ = ?
            WHERE user_id_ = ?
        """

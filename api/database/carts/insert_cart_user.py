from api.database.operation import DatabaseOperation


class CartInsertCartUserOperation(DatabaseOperation):
    def run(self, cart_id: int, user_id: int):
        self.cursor.execute(self.query, (cart_id, user_id))

    @property
    def query(self) -> str:
        return """
            INSERT INTO carts_users_ (cart_id_, user_id_)
            VALUES (?, ?)
        """

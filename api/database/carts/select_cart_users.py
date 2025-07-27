from api.database.operation import DatabaseOperation


class CartSelectCartUsersOperation(DatabaseOperation):
    def run(self, cart_id: int) -> set[int]:
        result = self.cursor.execute(self.query, (cart_id,))
        results = result.fetchall()
        return {(columns[0]) for columns in results}

    @property
    def query(self) -> str:
        return """
            SELECT user_id_
            FROM carts_users_
            WHERE cart_id_ = ?
        """

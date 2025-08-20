from api.database.operation import DatabaseOperation


class CartUpdateDefaultCartOperation(DatabaseOperation):
    def run(self, cart_id: int):
        self.cursor.execute(self.query, (cart_id,))

    @property
    def query(self) -> str:
        return """
            INSERT INTO metadata_ (metadata_id_, cart_id_)
            VALUES (0, ?)
            ON CONFLICT(metadata_id_) DO UPDATE SET cart_id_=excluded.cart_id_;
        """

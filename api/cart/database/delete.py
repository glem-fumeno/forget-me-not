from api.core.call import Call


class CartDeleteCall(Call):
    def run(self, item_id: int, origin: str):
        self.cursor.execute(self.query, (item_id, origin))

    @property
    def query(self) -> str:
        return """
            DELETE FROM cart_items_ WHERE item_id_ = ? AND origin_ = ?
        """

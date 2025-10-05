from api.core.call import Call


class CartInsertManyCall(Call):
    def run(self, origin: str, item_ids: set[int]):
        self.cursor.executemany(
            self.query, [(item_id, origin) for item_id in item_ids]
        )

    @property
    def query(self) -> str:
        return """
            INSERT INTO cart_items_ (item_id_, origin_) VALUES (?, ?)
        """

from api.core.call import Call


class CartSelectManyCall(Call):
    def run(self) -> set[tuple[int, str]]:
        cursor = self.cursor.execute(self.query)
        results = cursor.fetchall()
        return {(item_id, origin) for (item_id, origin) in results}

    @property
    def query(self) -> str:
        return """
            SELECT item_id_, origin_ FROM cart_items_
        """

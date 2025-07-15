from api.database.operation import DatabaseOperation


class ItemSelectItemByNameOperation(DatabaseOperation):
    def run(self, name: str) -> int | None:
        result = self.cursor.execute(self.query, (name,))
        columns = result.fetchone()
        if columns is None:
            return
        return columns[0]

    @property
    def query(self) -> str:
        return """
            SELECT item_id_ FROM items_ WHERE name_ = ?
        """

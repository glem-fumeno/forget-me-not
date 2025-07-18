from api.database.operation import DatabaseOperation


class ItemDeleteItemOperation(DatabaseOperation):
    def run(self, item_id: int):
        self.cursor.execute(self.query, (item_id,))

    @property
    def query(self) -> str:
        return """
            DELETE FROM items_ WHERE item_id_ = ?
        """

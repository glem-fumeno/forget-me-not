from api.database.operation import DatabaseOperation
from api.models.items.models import ItemModel


class ItemInsertItemOperation(DatabaseOperation):
    def run(self, model: ItemModel):
        result = self.cursor.execute(self.query, model.parameters)
        assert result.lastrowid is not None, "could not insert item"
        model.item_id = result.lastrowid

    @property
    def query(self) -> str:
        return """
            INSERT INTO items_ (name_, icon_)
            VALUES (?, ?)
        """

from api.database.operation import DatabaseOperation
from api.models.items.models import ItemModel


class ItemUpdateItemOperation(DatabaseOperation):
    def run(self, model: ItemModel):
        self.cursor.execute(self.query, (*model.parameters, model.item_id))

    @property
    def query(self) -> str:
        return """
            UPDATE items_
            SET
                name_ = ?,
                icon_ = ?
            WHERE
                item_id_ = ?
        """

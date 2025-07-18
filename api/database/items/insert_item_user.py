from api.database.operation import DatabaseOperation
from api.models.items.models import ItemUserModel


class ItemInsertItemUserOperation(DatabaseOperation):
    def run(self, model: ItemUserModel):
        self.cursor.execute(self.query, model.parameters)

    @property
    def query(self) -> str:
        return """
            INSERT INTO items_users_ (item_id_, user_id_)
            VALUES (?, ?)
        """

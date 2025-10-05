from api.core.call import Call
from api.items.models import ItemModel


class ItemInsertCall(Call):
    def run(self, model: ItemModel):
        cursor = self.cursor.execute(self.query, (model.name, model.icon))
        (item_id,) = cursor.fetchone()
        model.item_id = item_id

    @property
    def query(self) -> str:
        return """
            INSERT INTO items_ (name_, icon_) VALUES (?, ?) RETURNING item_id_
        """

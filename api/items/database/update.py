from api.core.call import Call
from api.items.models import ItemModel


class ItemUpdateCall(Call):
    def run(self, model: ItemModel):
        self.cursor.execute(
            self.query, (model.name, model.icon, model.item_id)
        )

    @property
    def query(self) -> str:
        return """
            UPDATE items_ SET name_ = ?, icon_ = ?
            WHERE item_id_ = ?
        """

from api.core.call import Call
from api.items.models import ItemModel


class ItemSelectCall(Call):
    def run(self, item_id: int) -> ItemModel | None:
        cursor = self.cursor.execute(self.query, (item_id,))
        result = cursor.fetchone()
        if result is None:
            return
        (name, icon) = result
        return ItemModel(item_id, name, icon)

    @property
    def query(self) -> str:
        return """
            SELECT name_, icon_ FROM items_ WHERE item_id_ = ?
        """

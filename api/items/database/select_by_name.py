from api.core.call import Call
from api.items.models import ItemModel


class ItemSelectByNameCall(Call):
    def run(self, name: str) -> ItemModel | None:
        cursor = self.cursor.execute(self.query, (name,))
        result = cursor.fetchone()
        if result is None:
            return
        (item_id, icon) = result
        return ItemModel(item_id, name, icon)

    @property
    def query(self) -> str:
        return """
            SELECT item_id_, icon_ FROM items_ WHERE name_ = ?
        """

from api.core.call import Call
from api.items.models import ItemModel


class ItemSelectManyCall(Call):
    def run(self) -> dict[int, ItemModel]:
        cursor = self.cursor.execute(self.query)
        results = cursor.fetchall()
        return {
            item_id: ItemModel(item_id, name, icon)
            for (item_id, name, icon) in results
        }

    @property
    def query(self) -> str:
        return """
            SELECT item_id_, name_, icon_ FROM items_
        """

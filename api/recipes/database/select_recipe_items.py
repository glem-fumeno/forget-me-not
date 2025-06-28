from api.database.operation import DatabaseOperation
from api.items.schemas.models import ItemModel


class RecipeSelectRecipeItemsOperation(DatabaseOperation):
    def run(self, recipe_id: int) -> list[ItemModel]:
        result = self.cursor.execute(self.query, (recipe_id,))
        results = result.fetchall()
        return [
            ItemModel.from_db(result.description, columns)
            for columns in results
        ]

    @property
    def query(self) -> str:
        return """
            SELECT item_id_, name_, icon_
            FROM items_
            INNER JOIN recipes_items_ USING (item_id_)
            WHERE recipe_id_ = ?
            ORDER BY name_
        """

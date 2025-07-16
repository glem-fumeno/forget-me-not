from api.database.operation import DatabaseOperation


class RecipeSelectRecipeItemsOperation(DatabaseOperation):
    def run(self, recipe_id: int) -> set[int]:
        result = self.cursor.execute(self.query, (recipe_id,))
        return {columns[0] for columns in result.fetchall()}

    @property
    def query(self) -> str:
        return """
            SELECT item_id_
            FROM recipes_items_
            WHERE recipe_id_ = ?
        """

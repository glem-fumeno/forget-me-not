from api.core.call import Call


class RecipeSelectItemsCall(Call):
    def run(self, recipe_id: int) -> set[int]:
        cursor = self.cursor.execute(self.query, (recipe_id,))
        results = cursor.fetchall()
        return {item_id for (item_id,) in results}

    @property
    def query(self) -> str:
        return """
            SELECT item_id_ FROM recipes_items_ WHERE recipe_id_ = ?
        """

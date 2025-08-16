from api.database.operation import DatabaseOperation


class RecipeSelectRecipeItemsOperation(DatabaseOperation):
    def run(self, recipe_ids: list[int]) -> list[set[int]]:
        self.ids = {recipe_id: set() for recipe_id in recipe_ids}
        results = self.cursor.execute(self.query, recipe_ids)
        for result in results.fetchall():
            self.ids[result[0]].add(result[1])
        return [self.ids[recipe_id] for recipe_id in recipe_ids]

    @property
    def query(self) -> str:
        return f"""
            SELECT recipe_id_, item_id_
            FROM recipes_items_
            WHERE recipe_id_ IN ({', '.join(['?' for _ in self.ids])})
        """

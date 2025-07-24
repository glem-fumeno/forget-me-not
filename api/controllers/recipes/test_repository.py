from api.controllers.test_repository import TestRepository
from api.models.recipes.models import RecipeModel, RecipeUserModel


class RecipeTestRepository(TestRepository):

    def insert_recipe(self, user_id: int, model: RecipeModel):
        self.max_recipe_id += 1
        self.recipe_map[self.max_recipe_id] = model
        self.recipe_name_map[user_id, model.name] = self.max_recipe_id
        model.recipe_id = self.max_recipe_id

    def insert_recipe_user(self, model: RecipeUserModel):
        if model.user_id not in self.user_recipe_map:
            self.user_recipe_map[model.user_id] = []
        self.user_recipe_map[model.user_id].append(model.recipe_id)

    def select_recipe_by_name(self, user_id: int, name: str) -> int | None:
        return self.recipe_name_map.get((user_id, name))

    def select_recipe(
        self, user_id: int, recipe_id: int
    ) -> RecipeModel | None:
        result = self.recipe_map.get(recipe_id)
        if (
            result is None
            or self.recipe_name_map.get((user_id, result.name)) != recipe_id
        ):
            return
        return result.copy()

    def insert_recipe_item(self, recipe_id: int, item_id: int):
        if recipe_id not in self.recipe_item_map:
            self.recipe_item_map[recipe_id] = set()
        self.recipe_item_map[recipe_id].add(item_id)

    def select_recipe_items(self, recipe_id: int) -> set[int]:
        return self.recipe_item_map[recipe_id]

    def delete_recipe_item(self, recipe_id: int, item_id: int):
        self.recipe_item_map[recipe_id].discard(item_id)

    def select_recipes(self, user_id: int) -> dict[int, RecipeModel]:
        return {
            recipe_id: self.recipe_map[recipe_id]
            for (recipe_user_id, _), recipe_id in self.recipe_name_map.items()
            if recipe_user_id == user_id
        }

    def update_recipe(self, model: RecipeModel):
        old_model = self.recipe_map[model.recipe_id]
        self.recipe_map[model.recipe_id] = model
        to_pop = set()
        for (user_id, _), recipe_id in self.recipe_name_map.items():
            if recipe_id == model.recipe_id:
                to_pop.add(user_id)
        for user_id in to_pop:
            self.recipe_name_map.pop((user_id, old_model.name), -1)
            self.recipe_name_map[user_id, model.name] = model.recipe_id

    def delete_recipe(self, recipe_id: int):
        result = self.recipe_map.pop(recipe_id, None)
        if result is None:
            return
        to_pop = set()
        for (user_id, _), old_recipe_id in self.recipe_name_map.items():
            if old_recipe_id == recipe_id:
                to_pop.add(user_id)
        for user_id in to_pop:
            self.recipe_name_map.pop((user_id, result.name), -1)

    def init_recipes(self):
        self.max_recipe_id: int = 0
        self.recipe_map: dict[int, RecipeModel] = {}
        self.recipe_name_map: dict[tuple[int, str], int] = {}
        self.user_recipe_map: dict[int, list[int]] = {}
        self.recipe_item_map: dict[int, set[int]] = {}

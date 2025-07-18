from api.models.items.models import ItemModel, ItemUserModel


class ItemTestRepository:

    def insert_item(self, model: ItemModel):
        self.max_item_id += 1
        self.item_map[self.max_item_id] = model
        self.item_name_map[model.name] = self.max_item_id
        model.item_id = self.max_item_id

    def insert_item_user(self, model: ItemUserModel):
        if model.user_id not in self.user_item_map:
            self.user_item_map[model.user_id] = []
        self.user_item_map[model.user_id].append(model.item_id)

    def select_item_by_name(self, name: str) -> int | None:
        return self.item_name_map.get(name)

    def select_item(self, item_id: int) -> ItemModel | None:
        result = self.item_map.get(item_id)
        if result is None:
            return
        return result.copy()

    def select_items(self) -> dict[int, ItemModel]:
        return self.item_map

    def update_item(self, model: ItemModel):
        old_model = self.item_map[model.item_id]
        self.item_map[model.item_id] = model
        self.item_name_map.pop(old_model.name, -1)
        self.item_name_map[model.name] = model.item_id

    def delete_item(self, item_id: int):
        result = self.item_map.pop(item_id, None)
        if result is None:
            return
        self.item_name_map.pop(result.name, None)

    def init_items(self):
        self.max_item_id: int = 0
        self.item_map: dict[int, ItemModel] = {}
        self.item_name_map: dict[str, int] = {}
        self.user_item_map: dict[int, list[int]] = {}

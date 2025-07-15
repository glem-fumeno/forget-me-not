from api.database.repository import DatabaseRepository
from api.database.items.delete_item import ItemDeleteItemOperation
from api.database.items.insert_item import ItemInsertItemOperation
from api.database.items.insert_item_user import ItemInsertItemUserOperation
from api.database.items.select_by_name_item import (
    ItemSelectItemByNameOperation,
)
from api.database.items.select_item import ItemSelectItemOperation
from api.database.items.select_items import ItemSelectItemsOperation
from api.database.items.update_item import ItemUpdateItemOperation
from api.models.items.models import ItemModel, ItemUserModel
from api.database.users.select_user_by_token import (
    UserSelectUserByTokenOperation,
)
from api.models.users.models import UserModel


class ItemDatabaseRepository(DatabaseRepository):
    def insert_item(self, model: ItemModel):
        return ItemInsertItemOperation(self.ctx, self.cursor).run(model)

    def insert_item_user(self, model: ItemUserModel):
        return ItemInsertItemUserOperation(self.ctx, self.cursor).run(model)

    def select_items(self) -> dict[int, ItemModel]:
        return ItemSelectItemsOperation(self.ctx, self.cursor).run()

    def select_item(self, item_id: int) -> ItemModel | None:
        return ItemSelectItemOperation(self.ctx, self.cursor).run(item_id)

    def select_user_by_token(self, token: str) -> UserModel | None:
        return UserSelectUserByTokenOperation(self.ctx, self.cursor).run(token)

    def select_item_by_name(self, name: str) -> int | None:
        return ItemSelectItemByNameOperation(self.ctx, self.cursor).run(name)

    def update_item(self, model: ItemModel):
        return ItemUpdateItemOperation(self.ctx, self.cursor).run(model)

    def delete_item(self, item_id: int):
        return ItemDeleteItemOperation(self.ctx, self.cursor).run(item_id)

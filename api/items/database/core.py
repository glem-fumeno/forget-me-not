from api.database.repository import DatabaseRepository
from api.items.database.delete_item import ItemDeleteItemOperation
from api.items.database.insert_item import ItemInsertItemOperation
from api.items.database.insert_item_user import (
    ItemInsertItemUserOperation,
)
from api.items.database.select_by_name_item import (
    ItemSelectItemByNameOperation,
)
from api.items.database.select_item import ItemSelectItemOperation
from api.items.database.select_items import ItemSelectItemsOperation
from api.items.database.update_item import ItemUpdateItemOperation
from api.items.schemas.models import ItemModel, ItemUserModel
from api.users.database.select_user_by_token import (
    UserSelectUserByTokenOperation,
)
from api.users.schemas.models import UserModel


class ItemDatabaseRepository(DatabaseRepository):
    def insert_item(self, model: ItemModel):
        return ItemInsertItemOperation(self.cursor).run(model)

    def insert_item_user(self, model: ItemUserModel):
        return ItemInsertItemUserOperation(self.cursor).run(model)

    def select_items(self) -> dict[int, ItemModel]:
        return ItemSelectItemsOperation(self.cursor).run()

    def select_item(self, item_id: int) -> ItemModel | None:
        return ItemSelectItemOperation(self.cursor).run(item_id)

    def select_user_by_token(self, token: str) -> UserModel | None:
        return UserSelectUserByTokenOperation(self.cursor).run(token)

    def select_item_by_name(self, name: str) -> int | None:
        return ItemSelectItemByNameOperation(self.cursor).run(name)

    def update_item(self, model: ItemModel):
        return ItemUpdateItemOperation(self.cursor).run(model)

    def delete_item(self, item_id: int):
        return ItemDeleteItemOperation(self.cursor).run(item_id)

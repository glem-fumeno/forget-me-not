from api.database.facade import Facade
from api.database.items.delete_item import ItemDeleteItemOperation
from api.database.items.insert_item import ItemInsertItemOperation
from api.database.items.insert_item_user import ItemInsertItemUserOperation
from api.database.items.select_by_name_item import (
    ItemSelectItemByNameOperation,
)
from api.database.items.select_item import ItemSelectItemOperation
from api.database.items.select_items import ItemSelectItemsOperation
from api.database.items.update_item import ItemUpdateItemOperation


class ItemRepository(Facade):
    insert_item = ItemInsertItemOperation.run
    insert_item_user = ItemInsertItemUserOperation.run
    select_items = ItemSelectItemsOperation.run
    select_item = ItemSelectItemOperation.run
    select_item_by_name = ItemSelectItemByNameOperation.run
    update_item = ItemUpdateItemOperation.run
    delete_item = ItemDeleteItemOperation.run

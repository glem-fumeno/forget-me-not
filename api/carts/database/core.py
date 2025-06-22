from api.carts.database.delete_cart import CartDeleteCartOperation
from api.carts.database.delete_cart_item import CartDeleteCartItemOperation
from api.carts.database.insert_cart import CartInsertCartOperation
from api.carts.database.insert_cart_item import CartInsertCartItemOperation
from api.carts.database.insert_cart_user import (
    CartInsertCartUserOperation,
)
from api.carts.database.select_cart import CartSelectCartOperation
from api.carts.database.select_cart_items import CartSelectCartItemsOperation
from api.carts.database.select_carts import CartSelectCartsOperation
from api.carts.database.update_cart import CartUpdateCartOperation
from api.carts.schemas.models import CartModel, CartUserModel
from api.database.repository import DatabaseRepository
from api.items.database.select_items import ItemSelectItemsOperation
from api.items.schemas.models import ItemModel
from api.users.database.select_user_by_token import (
    UserSelectUserByTokenOperation,
)
from api.users.schemas.models import UserModel


class CartDatabaseRepository(DatabaseRepository):
    def insert_cart(self, user_id: int, model: CartModel):
        return CartInsertCartOperation(self.cursor).run(user_id, model)

    def insert_cart_user(self, model: CartUserModel):
        return CartInsertCartUserOperation(self.cursor).run(model)

    def insert_cart_item(self, cart_id: int, item_id: int):
        return CartInsertCartItemOperation(self.cursor).run(cart_id, item_id)

    def select_items(self) -> dict[int, ItemModel]:
        return ItemSelectItemsOperation(self.cursor).run()

    def select_carts(self, user_id: int) -> dict[int, CartModel]:
        return CartSelectCartsOperation(self.cursor).run(user_id)

    def select_cart_items(self, cart_id: int) -> list[ItemModel]:
        return CartSelectCartItemsOperation(self.cursor).run(cart_id)

    def select_cart(self, user_id: int, cart_id: int) -> CartModel | None:
        return CartSelectCartOperation(self.cursor).run(user_id, cart_id)

    def select_user_by_token(self, token: str) -> UserModel | None:
        return UserSelectUserByTokenOperation(self.cursor).run(token)

    def update_cart(self, model: CartModel):
        return CartUpdateCartOperation(self.cursor).run(model)

    def delete_cart(self, cart_id: int):
        return CartDeleteCartOperation(self.cursor).run(cart_id)

    def delete_cart_item(self, cart_id: int, item_id: int):
        return CartDeleteCartItemOperation(self.cursor).run(cart_id, item_id)

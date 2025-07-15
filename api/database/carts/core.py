from api.database.carts.delete_cart import CartDeleteCartOperation
from api.database.carts.delete_cart_item import CartDeleteCartItemOperation
from api.database.carts.insert_cart import CartInsertCartOperation
from api.database.carts.insert_cart_item import CartInsertCartItemOperation
from api.database.carts.insert_cart_user import CartInsertCartUserOperation
from api.database.carts.select_cart import CartSelectCartOperation
from api.database.carts.select_cart_items import CartSelectCartItemsOperation
from api.database.carts.select_carts import CartSelectCartsOperation
from api.database.carts.update_cart import CartUpdateCartOperation
from api.models.carts.models import CartModel, CartUserModel
from api.database.repository import DatabaseRepository
from api.database.items.select_items import ItemSelectItemsOperation
from api.models.items.models import ItemModel
from api.database.users.select_user_by_token import (
    UserSelectUserByTokenOperation,
)
from api.models.users.models import UserModel


class CartDatabaseRepository(DatabaseRepository):
    def insert_cart(self, user_id: int, model: CartModel):
        return CartInsertCartOperation(self.ctx, self.cursor).run(
            user_id, model
        )

    def insert_cart_user(self, model: CartUserModel):
        return CartInsertCartUserOperation(self.ctx, self.cursor).run(model)

    def insert_cart_item(self, cart_id: int, item_id: int):
        return CartInsertCartItemOperation(self.ctx, self.cursor).run(
            cart_id, item_id
        )

    def select_items(self) -> dict[int, ItemModel]:
        return ItemSelectItemsOperation(self.ctx, self.cursor).run()

    def select_carts(self, user_id: int) -> dict[int, CartModel]:
        return CartSelectCartsOperation(self.ctx, self.cursor).run(user_id)

    def select_cart_items(self, cart_id: int) -> list[ItemModel]:
        return CartSelectCartItemsOperation(self.ctx, self.cursor).run(cart_id)

    def select_cart(self, user_id: int, cart_id: int) -> CartModel | None:
        return CartSelectCartOperation(self.ctx, self.cursor).run(
            user_id, cart_id
        )

    def select_user_by_token(self, token: str) -> UserModel | None:
        return UserSelectUserByTokenOperation(self.ctx, self.cursor).run(token)

    def update_cart(self, model: CartModel):
        return CartUpdateCartOperation(self.ctx, self.cursor).run(model)

    def delete_cart(self, cart_id: int):
        return CartDeleteCartOperation(self.ctx, self.cursor).run(cart_id)

    def delete_cart_item(self, cart_id: int, item_id: int):
        return CartDeleteCartItemOperation(self.ctx, self.cursor).run(
            cart_id, item_id
        )

from api.controllers.test_repository import TestRepository
from api.models.carts.models import CartModel


class CartTestRepository(TestRepository):

    def init_carts(self):
        self.max_cart_id: int = 0
        self.cart_map: dict[int, CartModel] = {}
        self.cart_name_map: dict[tuple[int, str], int] = {}
        self.user_cart_map: dict[int, list[int]] = {}
        self.cart_item_map: dict[int, set[tuple[int, str]]] = {}

    def insert_cart(self, user_id: int, model: CartModel):
        self.max_cart_id += 1
        self.cart_map[self.max_cart_id] = model
        self.cart_name_map[user_id, model.name] = self.max_cart_id
        self.cart_item_map[self.max_cart_id] = set()
        self.user_cart_map[user_id] = [self.max_cart_id]
        model.cart_id = self.max_cart_id

    def insert_cart_user(self, cart_id: int, user_id: int):
        if user_id not in self.user_cart_map:
            self.user_cart_map[user_id] = []
        self.user_cart_map[user_id].append(cart_id)
        self.cart_name_map[user_id, self.cart_map[cart_id].name] = cart_id

    def delete_cart_user(self, cart_id: int, user_id: int):
        if user_id not in self.user_cart_map:
            return
        self.user_cart_map[user_id].remove(cart_id)
        self.cart_name_map.pop((user_id, self.cart_map[cart_id].name))

    def select_cart_by_name(self, user_id: int, name: str) -> int | None:
        return self.cart_name_map.get((user_id, name))

    def select_cart(self, user_id: int, cart_id: int) -> CartModel | None:
        result = self.cart_map.get(cart_id)
        if (
            result is None
            or self.cart_name_map.get((user_id, result.name)) != cart_id
        ):
            return
        return result.copy()

    def insert_cart_items(self, cart_id: int, item_ids: set[int], origin: str):
        if cart_id not in self.cart_item_map:
            self.cart_item_map[cart_id] = set()
        self.cart_item_map[cart_id] = self.cart_item_map[cart_id].union(
            {(item_id, origin) for item_id in item_ids}
        )

    def select_cart_users(self, cart_id: int) -> set[int]:
        return {
            user_id
            for (user_id, _), cid in self.cart_name_map.items()
            if cid == cart_id
        }

    def select_cart_items(self, cart_id: int) -> set[tuple[int, str]]:
        return self.cart_item_map[cart_id]

    def delete_cart_item(self, cart_id: int, item_id: int, origin: str):
        self.cart_item_map[cart_id].remove((item_id, origin))

    def select_carts(self, user_id: int) -> dict[int, CartModel]:
        return {
            cart_id: self.cart_map[cart_id]
            for (cart_user_id, _), cart_id in self.cart_name_map.items()
            if cart_user_id == user_id
        }

    def update_cart(self, model: CartModel):
        old_model = self.cart_map[model.cart_id]
        self.cart_map[model.cart_id] = model
        to_pop = set()
        for (user_id, _), cart_id in self.cart_name_map.items():
            if cart_id == model.cart_id:
                to_pop.add(user_id)
        for user_id in to_pop:
            self.cart_name_map.pop((user_id, old_model.name), -1)
            self.cart_name_map[user_id, model.name] = model.cart_id

    def delete_cart(self, cart_id: int):
        result = self.cart_map.pop(cart_id, None)
        if result is None:
            return
        to_pop = set()
        for (user_id, _), old_cart_id in self.cart_name_map.items():
            if old_cart_id == cart_id:
                to_pop.add(user_id)
        for user_id in to_pop:
            self.cart_name_map.pop((user_id, result.name), -1)

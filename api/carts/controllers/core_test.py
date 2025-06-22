from api.carts.schemas.models import CartModel, CartUserModel
from api.items.schemas.models import ItemModel
from api.users.common import get_hash, get_uuid
from api.users.schemas.models import RoleLiteral, UserModel


class CartTestRepository:
    def __init__(self) -> None:
        super().__init__()
        self.init_users()
        self.init_items()
        self.init_carts()

    def insert_cart(self, user_id: int, model: CartModel):
        self.max_cart_id += 1
        self.cart_map[self.max_cart_id] = model
        self.cart_name_map[user_id, model.name] = self.max_cart_id
        model.cart_id = self.max_cart_id

    def insert_cart_user(self, model: CartUserModel):
        if model.user_id not in self.user_cart_map:
            self.user_cart_map[model.user_id] = []
        self.user_cart_map[model.user_id].append(model.cart_id)

    def select_user_by_token(self, token: str) -> UserModel | None:
        user_id = self.user_login_map.get(token)
        if user_id is None:
            return
        return self.user_map[user_id]

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

    def insert_cart_item(self, cart_id: int, item_id: int):
        if cart_id not in self.cart_item_map:
            self.cart_item_map[cart_id] = set()
        self.cart_item_map[cart_id].add(item_id)

    def select_cart_items(self, cart_id: int) -> list[ItemModel]:
        return [
            self.item_map[item_id] for item_id in self.cart_item_map[cart_id]
        ]

    def delete_cart_item(self, cart_id: int, item_id: int):
        self.cart_item_map[cart_id].discard(item_id)

    def select_items(self) -> dict[int, ItemModel]:
        return self.item_map

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

    def init_users(self):
        self.max_user_id: int = 0
        self.user_map: dict[int, UserModel] = {}
        self.email_map: dict[str, int] = {}
        self.user_login_map: dict[str, int] = {}

        self.__insert_user(
            "aanderson", "alice.anderson@example.com", "A1ice_89rocks", "admin"
        )
        self.__insert_user(
            "b.baker92", "bob.baker@example.com", "SunsetDrive@34", "user"
        )

    def init_items(self):
        self.max_item_id: int = 0
        self.item_map: dict[int, ItemModel] = {}
        self.item_name_map: dict[str, int] = {}
        self.user_item_map: dict[int, list[int]] = {}

        self.__insert_item(
            "milk", "https://img.icons8.com/pulsar-line/96/milk.png"
        )
        self.__insert_item(
            "rice", "https://img.icons8.com/pulsar-line/96/rice-bowl.png"
        )
        self.__insert_item(
            "soap", "https://img.icons8.com/pulsar-line/96/soap.png"
        )

    def init_carts(self):
        self.max_cart_id: int = 0
        self.cart_map: dict[int, CartModel] = {}
        self.cart_name_map: dict[tuple[int, str], int] = {}
        self.user_cart_map: dict[int, list[int]] = {}
        self.cart_item_map: dict[int, set[int]] = {}

        self.__insert_cart(
            "alice.anderson@example.com",
            "groceries",
            "https://img.icons8.com/pulsar-line/96/shopping-cart.png",
        )
        self.__insert_cart(
            "alice.anderson@example.com",
            "gift for bob",
            "https://img.icons8.com/pulsar-line/96/gift.png",
        )
        self.__insert_cart_user(
            "alice.anderson@example.com", "groceries", "bob.baker@example.com"
        )
        self.__insert_cart_item(
            "alice.anderson@example.com", "groceries", "rice"
        )
        self.__insert_cart_item("bob.baker@example.com", "groceries", "milk")
        self.__insert_cart_item(
            "alice.anderson@example.com", "gift for bob", "soap"
        )

    def login(self, user_id: int):
        token = get_uuid()
        self.user_login_map[token] = user_id
        return token

    def __insert_user(
        self, username: str, email: str, password: str, role: RoleLiteral
    ):
        self.max_user_id += 1
        self.user_map[self.max_user_id] = UserModel(
            self.max_user_id, username, email, get_hash(password), role
        )
        self.email_map[email] = self.max_user_id

    def __insert_item(self, name: str, icon: str):
        self.max_item_id += 1
        self.item_map[self.max_item_id] = ItemModel(
            self.max_item_id, name, icon
        )
        self.item_name_map[name] = self.max_item_id

    def __insert_cart(self, owner: str, name: str, icon: str):
        user_id = self.email_map[owner]
        self.max_cart_id += 1
        self.cart_map[self.max_cart_id] = CartModel(
            self.max_cart_id, name, icon
        )
        self.cart_name_map[user_id, name] = self.max_cart_id
        self.__insert_cart_user(owner, name, owner)

    def __insert_cart_user(self, owner: str, cart: str, user: str):
        owner_id = self.email_map[owner]
        cart_id = self.cart_name_map[owner_id, cart]
        user_id = self.email_map[user]
        if user_id not in self.user_cart_map:
            self.user_cart_map[user_id] = []
        self.user_cart_map[user_id].append(cart_id)
        self.cart_name_map[user_id, cart] = cart_id

    def __insert_cart_item(self, user: str, cart: str, item: str):
        user_id = self.email_map[user]
        cart_id = self.cart_name_map[user_id, cart]
        item_id = self.item_name_map[item]
        if cart_id not in self.cart_item_map:
            self.cart_item_map[cart_id] = set()
        self.cart_item_map[cart_id].add(item_id)

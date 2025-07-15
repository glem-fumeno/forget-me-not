from api.models.items.models import ItemModel, ItemUserModel
from api.security import get_hash, get_uuid
from api.models.users.models import RoleLiteral, UserModel


class ItemTestRepository:
    def __init__(self) -> None:
        super().__init__()
        self.init_users()
        self.init_items()

    def insert_item(self, model: ItemModel):
        self.max_item_id += 1
        self.item_map[self.max_item_id] = model
        self.item_name_map[model.name] = self.max_item_id
        model.item_id = self.max_item_id

    def insert_item_user(self, model: ItemUserModel):
        if model.user_id not in self.user_item_map:
            self.user_item_map[model.user_id] = []
        self.user_item_map[model.user_id].append(model.item_id)

    def select_user_by_token(self, token: str) -> UserModel | None:
        user_id = self.user_login_map.get(token)
        if user_id is None:
            return
        return self.user_map[user_id]

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
        self.__insert_item_user("rice", "alice.anderson@example.com")
        self.__insert_item_user("milk", "alice.anderson@example.com")
        self.__insert_item_user("rice", "bob.baker@example.com")

    def login(self, user_id: int):
        token = get_uuid()
        self.user_login_map[token] = user_id
        return token

    def __insert_user(
        self, username: str, email: str, password: str, role: RoleLiteral
    ):
        self.max_user_id += 1
        self.user_map[self.max_user_id] = UserModel(
            user_id=self.max_user_id,
            username=username,
            email=email,
            password=get_hash(password),
            role=role,
        )
        self.email_map[email] = self.max_user_id

    def __insert_item(self, name: str, icon: str):
        self.max_item_id += 1
        self.item_map[self.max_item_id] = ItemModel(
            item_id=self.max_item_id, name=name, icon=icon
        )
        self.item_name_map[name] = self.max_item_id

    def __insert_item_user(self, item: str, user: str):
        item_id = self.item_name_map[item]
        user_id = self.email_map[user]
        if user_id not in self.user_item_map:
            self.user_item_map[user_id] = []
        self.user_item_map[user_id].append(item_id)

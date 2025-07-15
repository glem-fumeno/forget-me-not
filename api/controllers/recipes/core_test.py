from api.models.items.models import ItemModel
from api.models.recipes.models import RecipeModel, RecipeUserModel
from api.security import get_hash, get_uuid
from api.models.users.models import RoleLiteral, UserModel


class RecipeTestRepository:
    def __init__(self) -> None:
        super().__init__()
        self.init_users()
        self.init_items()
        self.init_recipes()

    def insert_recipe(self, user_id: int, model: RecipeModel):
        self.max_recipe_id += 1
        self.recipe_map[self.max_recipe_id] = model
        self.recipe_name_map[user_id, model.name] = self.max_recipe_id
        model.recipe_id = self.max_recipe_id

    def insert_recipe_user(self, model: RecipeUserModel):
        if model.user_id not in self.user_recipe_map:
            self.user_recipe_map[model.user_id] = []
        self.user_recipe_map[model.user_id].append(model.recipe_id)

    def select_user_by_token(self, token: str) -> UserModel | None:
        user_id = self.user_login_map.get(token)
        if user_id is None:
            return
        return self.user_map[user_id]

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

    def select_recipe_items(self, recipe_id: int) -> list[ItemModel]:
        return [
            self.item_map[item_id]
            for item_id in self.recipe_item_map[recipe_id]
        ]

    def delete_recipe_item(self, recipe_id: int, item_id: int):
        self.recipe_item_map[recipe_id].discard(item_id)

    def select_items(self) -> dict[int, ItemModel]:
        return self.item_map

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
            "eggs", "https://img.icons8.com/pulsar-line/96/eggs.png"
        )
        self.__insert_item(
            "flour",
            "https://img.icons8.com/pulsar-line/96/flour-in-paper-packaging.png",
        )

    def init_recipes(self):
        self.max_recipe_id: int = 0
        self.recipe_map: dict[int, RecipeModel] = {}
        self.recipe_name_map: dict[tuple[int, str], int] = {}
        self.user_recipe_map: dict[int, list[int]] = {}
        self.recipe_item_map: dict[int, set[int]] = {}

        self.__insert_recipe(
            "alice.anderson@example.com",
            "pancakes",
            "https://img.icons8.com/pulsar-line/96/pancake.png",
        )
        self.__insert_recipe(
            "alice.anderson@example.com",
            "omlette",
            "https://img.icons8.com/pulsar-line/96/omlette.png",
        )
        self.__insert_recipe_user(
            "alice.anderson@example.com", "pancakes", "bob.baker@example.com"
        )
        self.__insert_recipe_item(
            "alice.anderson@example.com", "pancakes", "milk"
        )
        self.__insert_recipe_item(
            "alice.anderson@example.com", "pancakes", "flour"
        )
        self.__insert_recipe_item("bob.baker@example.com", "pancakes", "eggs")
        self.__insert_recipe_item(
            "alice.anderson@example.com", "omlette", "eggs"
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

    def __insert_recipe(self, owner: str, name: str, icon: str):
        user_id = self.email_map[owner]
        self.max_recipe_id += 1
        self.recipe_map[self.max_recipe_id] = RecipeModel(
            recipe_id=self.max_recipe_id, name=name, icon=icon
        )
        self.recipe_name_map[user_id, name] = self.max_recipe_id
        self.__insert_recipe_user(owner, name, owner)

    def __insert_recipe_user(self, owner: str, recipe: str, user: str):
        owner_id = self.email_map[owner]
        recipe_id = self.recipe_name_map[owner_id, recipe]
        user_id = self.email_map[user]
        if user_id not in self.user_recipe_map:
            self.user_recipe_map[user_id] = []
        self.user_recipe_map[user_id].append(recipe_id)
        self.recipe_name_map[user_id, recipe] = recipe_id

    def __insert_recipe_item(self, user: str, recipe: str, item: str):
        user_id = self.email_map[user]
        recipe_id = self.recipe_name_map[user_id, recipe]
        item_id = self.item_name_map[item]
        if recipe_id not in self.recipe_item_map:
            self.recipe_item_map[recipe_id] = set()
        self.recipe_item_map[recipe_id].add(item_id)

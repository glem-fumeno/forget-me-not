from api.controllers.carts.test_repository import CartTestRepository
from api.controllers.items.test_repository import ItemTestRepository
from api.controllers.recipes.test_repository import RecipeTestRepository
from api.controllers.users.test_repository import UserTestRepository
from api.models.carts.models import CartModel
from api.models.items.models import ItemModel
from api.models.recipes.models import RecipeModel
from api.models.users.models import RoleLiteral, UserModel
from api.security import get_hash


class MockRepository(
    UserTestRepository,
    RecipeTestRepository,
    ItemTestRepository,
    CartTestRepository,
):
    def __init__(self):
        self.init_users()
        self.init_items()
        self.init_recipes()
        self.init_carts()

    def init_users(self):
        super().init_users()
        self.__insert_user(
            "aanderson", "alice.anderson@example.com", "A1ice_89rocks", "admin"
        )
        self.__insert_user(
            "b.baker92", "bob.baker@example.com", "SunsetDrive@34", "user"
        )

    def init_items(self):
        super().init_items()
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
        self.__insert_item(
            "rice", "https://img.icons8.com/pulsar-line/96/rice-bowl.png"
        )
        self.__insert_item(
            "soap", "https://img.icons8.com/pulsar-line/96/soap.png"
        )
        self.__insert_item_user("rice", "alice.anderson@example.com")
        self.__insert_item_user("milk", "alice.anderson@example.com")
        self.__insert_item_user("rice", "bob.baker@example.com")

    def init_recipes(self):
        super().init_recipes()

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

    def init_carts(self):
        super().init_carts()

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

    def __insert_cart(self, owner: str, name: str, icon: str):
        user_id = self.email_map[owner]
        self.max_cart_id += 1
        self.cart_map[self.max_cart_id] = CartModel(
            cart_id=self.max_cart_id, name=name, icon=icon
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

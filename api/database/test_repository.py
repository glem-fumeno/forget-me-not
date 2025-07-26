from api.database.repository import DatabaseRepository
from api.models.carts.models import CartModel
from api.models.items.models import ItemModel
from api.models.recipes.models import RecipeModel
from api.models.users.models import RoleLiteral, UserModel, UserSessionModel
from api.security import get_hash


class DatabaseTestRepository(DatabaseRepository):

    def initialize_test_cases(self):
        self.user_map: dict[int, UserModel] = {}
        self.email_map: dict[str, int] = {}
        self.item_map: dict[int, ItemModel] = {}
        self.item_name_map: dict[str, int] = {}
        self.recipe_map: dict[int, RecipeModel] = {}
        self.recipe_name_map: dict[tuple[int, str], int] = {}
        self.cart_map: dict[int, CartModel] = {}
        self.cart_name_map: dict[tuple[int, str], int] = {}

        self.__insert_user(
            "aanderson", "alice.anderson@example.com", "A1ice_89rocks", "admin"
        )
        self.__insert_user(
            "b.baker92", "bob.baker@example.com", "SunsetDrive@34", "user"
        )
        self.__insert_session(
            "alice.anderson@example.com", "f77e3ce3430c4aeba5cc273089075c81"
        )
        self.__insert_item(
            "milk", "https://img.icons8.com/pulsar-line/96/milk.png"
        )
        self.__insert_item(
            "eggs", "https://img.icons8.com/pulsar-line/96/eggs.png"
        )
        self.__insert_item(
            "rice", "https://img.icons8.com/pulsar-line/96/rice-bowl.png"
        )
        self.__insert_item(
            "soap", "https://img.icons8.com/pulsar-line/96/soap.png"
        )
        self.__insert_item(
            "flour",
            "https://img.icons8.com/pulsar-line/96/flour-in-paper-packaging.png",
        )
        self.__insert_item_user("rice", "alice.anderson@example.com")
        self.__insert_item_user("milk", "alice.anderson@example.com")
        self.__insert_item_user("rice", "bob.baker@example.com")
        self.__insert_recipe(
            "alice.anderson@example.com",
            "pancakes",
            "https://img.icons8.com/pulsar-line/96/pancake.png",
        )
        self.__insert_recipe_user(
            "alice.anderson@example.com",
            "pancakes",
            "alice.anderson@example.com",
        )
        self.__insert_recipe(
            "alice.anderson@example.com",
            "omlette",
            "https://img.icons8.com/pulsar-line/96/omlette.png",
        )
        self.__insert_recipe_user(
            "alice.anderson@example.com",
            "omlette",
            "alice.anderson@example.com",
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
            "alice.anderson@example.com",
            "groceries",
            "alice.anderson@example.com",
        )
        self.__insert_cart_user(
            "alice.anderson@example.com",
            "gift for bob",
            "alice.anderson@example.com",
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

    def __insert_item_user(self, item: str, user: str):
        item_id = self.item_name_map[item]
        user_id = self.email_map[user]
        self.cursor.execute(self.__item_user_query, (item_id, user_id))

    @property
    def __item_user_query(self) -> str:
        return """
            INSERT INTO items_users_ (item_id_, user_id_)
            VALUES (?, ?)
        """

    def __insert_user(
        self, username: str, email: str, password: str, role: RoleLiteral
    ):
        model = UserModel(
            user_id=-1,
            cart_id=None,
            username=username,
            email=email,
            password=get_hash(password),
            role=role,
        )
        result = self.cursor.execute(self.__user_query, model.parameters)
        assert result.lastrowid is not None
        model.user_id = result.lastrowid
        self.user_map[model.user_id] = model
        self.email_map[email] = model.user_id

    def __insert_session(self, email: str, token: str):
        model = UserSessionModel(user_id=self.email_map[email], token=token)
        self.cursor.execute(self.__session_query, model.parameters)

    @property
    def __session_query(self) -> str:
        return """
            INSERT INTO users_sessions_ (user_id_, token_)
            VALUES (?, ?)
        """

    @property
    def __user_query(self) -> str:
        return """
            INSERT INTO users_ (username_, email_, password_, role_)
            VALUES (?, ?, ?, ?)
        """

    def __insert_item(self, name: str, icon: str):
        model = ItemModel(item_id=-1, name=name, icon=icon)
        result = self.cursor.execute(self.__item_query, model.parameters)
        assert result.lastrowid is not None
        model.item_id = result.lastrowid
        self.item_map[model.item_id] = model
        self.item_name_map[name] = model.item_id

    @property
    def __item_query(self) -> str:
        return """
            INSERT INTO items_ (name_, icon_)
            VALUES (?, ?)
        """

    def __insert_recipe(self, user: str, name: str, icon: str):
        user_id = self.email_map[user]
        model = RecipeModel(recipe_id=-1, name=name, icon=icon)
        result = self.cursor.execute(self.__recipe_query, model.parameters)
        assert result.lastrowid is not None
        model.recipe_id = result.lastrowid
        self.recipe_map[model.recipe_id] = model
        self.recipe_name_map[user_id, name] = model.recipe_id

    @property
    def __recipe_query(self) -> str:
        return """
            INSERT INTO recipes_ (name_, icon_)
            VALUES (?, ?)
        """

    def __insert_recipe_user(self, owner: str, recipe: str, user: str):
        owner_id = self.email_map[owner]
        recipe_id = self.recipe_name_map[owner_id, recipe]
        user_id = self.email_map[user]
        self.recipe_name_map[user_id, recipe] = recipe_id
        self.cursor.execute(self.__recipe_user_query, (recipe_id, user_id))

    @property
    def __recipe_user_query(self) -> str:
        return """
            INSERT INTO recipes_users_ (recipe_id_, user_id_)
            VALUES (?, ?)
        """

    def __insert_recipe_item(self, user: str, recipe: str, item: str):
        user_id = self.email_map[user]
        recipe_id = self.recipe_name_map[user_id, recipe]
        item_id = self.item_name_map[item]
        self.cursor.execute(self.__recipe_item_query, (recipe_id, item_id))

    @property
    def __recipe_item_query(self) -> str:
        return """
            INSERT INTO recipes_items_ (recipe_id_, item_id_)
            VALUES (?, ?)
        """

    def __insert_cart(self, user: str, name: str, icon: str):
        user_id = self.email_map[user]
        model = CartModel(cart_id=-1, name=name, icon=icon)
        result = self.cursor.execute(self.__cart_query, model.parameters)
        assert result.lastrowid is not None
        model.cart_id = result.lastrowid
        self.cart_map[model.cart_id] = model
        self.cart_name_map[user_id, name] = model.cart_id

    @property
    def __cart_query(self) -> str:
        return """
            INSERT INTO carts_ (name_, icon_)
            VALUES (?, ?)
        """

    def __insert_cart_user(self, owner: str, cart: str, user: str):
        owner_id = self.email_map[owner]
        cart_id = self.cart_name_map[owner_id, cart]
        user_id = self.email_map[user]
        self.cart_name_map[user_id, cart] = cart_id
        self.cursor.execute(self.__cart_user_query, (cart_id, user_id))

    @property
    def __cart_user_query(self) -> str:
        return """
            INSERT INTO carts_users_ (cart_id_, user_id_)
            VALUES (?, ?)
        """

    def __insert_cart_item(self, user: str, cart: str, item: str):
        user_id = self.email_map[user]
        cart_id = self.cart_name_map[user_id, cart]
        item_id = self.item_name_map[item]
        self.cursor.execute(self.__cart_item_query, (cart_id, item_id))

    @property
    def __cart_item_query(self) -> str:
        return """
            INSERT INTO carts_items_ (cart_id_, item_id_)
            VALUES (?, ?)
        """

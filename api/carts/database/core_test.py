from api.carts.database.core import CartDatabaseRepository
from api.carts.schemas.models import CartModel
from api.items.schemas.models import ItemModel
from api.users.common import get_hash
from api.users.schemas.models import RoleLiteral, UserModel


class CartDatabaseTestRepository(CartDatabaseRepository):

    def initialize_test_cases(self):
        self.user_map: dict[int, UserModel] = {}
        self.email_map: dict[str, int] = {}
        self.item_map: dict[int, ItemModel] = {}
        self.item_name_map: dict[str, int] = {}
        self.cart_map: dict[int, CartModel] = {}
        self.cart_name_map: dict[tuple[int, str], int] = {}

        self.__insert_user(
            "aanderson", "alice.anderson@example.com", "A1ice_89rocks", "admin"
        )
        self.__insert_user(
            "b.baker92", "bob.baker@example.com", "SunsetDrive@34", "user"
        )
        self.__insert_item(
            "milk", "https://img.icons8.com/pulsar-line/96/milk.png"
        )
        self.__insert_item(
            "rice", "https://img.icons8.com/pulsar-line/96/rice-bowl.png"
        )
        self.__insert_item(
            "soap", "https://img.icons8.com/pulsar-line/96/soap.png"
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

    def __insert_user(
        self, username: str, email: str, password: str, role: RoleLiteral
    ):
        model = UserModel(-1, username, email, get_hash(password), role)
        result = self.cursor.execute(self.__user_query, model.parameters)
        assert result.lastrowid is not None
        model.user_id = result.lastrowid
        self.user_map[model.user_id] = model
        self.email_map[email] = model.user_id

    @property
    def __user_query(self) -> str:
        return """
            INSERT INTO users_ (username_, email_, password_, role_)
            VALUES (?, ?, ?, ?)
        """

    def __insert_item(self, name: str, icon: str):
        model = ItemModel(-1, name, icon)
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

    def __insert_cart(self, user: str, name: str, icon: str):
        user_id = self.email_map[user]
        model = CartModel(-1, name, icon)
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

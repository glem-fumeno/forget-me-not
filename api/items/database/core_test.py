from api.items.database.core import ItemDatabaseRepository
from api.items.schemas.models import ItemModel
from api.users.common import get_hash
from api.users.schemas.models import RoleLiteral, UserModel


class ItemDatabaseTestRepository(ItemDatabaseRepository):

    def initialize_test_cases(self):
        self.user_map: dict[int, UserModel] = {}
        self.email_map: dict[str, int] = {}
        self.item_map: dict[int, ItemModel] = {}
        self.item_name_map: dict[str, int] = {}

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
        self.__insert_item_user("rice", "alice.anderson@example.com")
        self.__insert_item_user("milk", "alice.anderson@example.com")
        self.__insert_item_user("rice", "bob.baker@example.com")

    def __insert_user(
        self, username: str, email: str, password: str, role: RoleLiteral
    ):
        model = UserModel(
            user_id=-1,
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

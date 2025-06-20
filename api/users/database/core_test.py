from api.users.common import get_hash
from api.users.database.core import UserDatabaseRepository
from api.users.schemas.models import UserModel


class UserDatabaseTestRepository(UserDatabaseRepository):

    def initialize_test_cases(self):
        self.user_map: dict[int, UserModel] = {}
        self.email_map: dict[str, int] = {}

        self.__insert_user(
            "aanderson", "alice.anderson@example.com", "A1ice_89rocks"
        )
        self.__insert_user(
            "b.baker92", "bob.baker@example.com", "SunsetDrive@34"
        )

    def __insert_user(self, username: str, email: str, password: str):
        model = UserModel(-1, username, email, get_hash(password))
        result = self.cursor.execute(self.__user_query, model.parameters)
        assert result.lastrowid is not None
        model.user_id = result.lastrowid
        self.user_map[model.user_id] = model
        self.email_map[email] = model.user_id

    @property
    def __user_query(self) -> str:
        return """
            INSERT INTO users_ (username_, email_, password_)
            VALUES (?, ?, ?)
        """

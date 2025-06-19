from hashlib import sha256

from api.users.database.core import UserDatabaseRepository
from api.users.schemas.models import UserModel
from config import CONFIG


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
        password = sha256((password + CONFIG["SALT"]).encode()).hexdigest()

        user_id = self.cursor.execute(
            self.__user_insert_query,
            (username, email, password),
        ).fetchone()
        self.user_map[user_id] = UserModel(user_id, username, email, password)
        self.email_map[email] = user_id

    @property
    def __user_insert_query(self) -> str:
        return """
            INSERT INTO users_
                (username_, email_, password_)
            VALUES
                (?, ?, ?)
            RETURNING user_id_
        """

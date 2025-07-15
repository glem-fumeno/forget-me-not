from api.security import get_hash
from api.database.users.core import UserDatabaseRepository
from api.models.users.models import RoleLiteral, UserModel, UserSessionModel


class UserDatabaseTestRepository(UserDatabaseRepository):

    def initialize_test_cases(self):
        self.user_map: dict[int, UserModel] = {}
        self.email_map: dict[str, int] = {}

        self.__insert_user(
            "aanderson", "alice.anderson@example.com", "A1ice_89rocks", "admin"
        )
        self.__insert_user(
            "b.baker92", "bob.baker@example.com", "SunsetDrive@34", "user"
        )
        self.__insert_session(
            "alice.anderson@example.com", "f77e3ce3430c4aeba5cc273089075c81"
        )

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

    def __insert_session(self, email: str, token: str):
        model = UserSessionModel(user_id=self.email_map[email], token=token)
        self.cursor.execute(self.__session_query, model.parameters)

    @property
    def __session_query(self) -> str:
        return """
            INSERT INTO users_sessions_ (user_id_, token_)
            VALUES (?, ?)
        """

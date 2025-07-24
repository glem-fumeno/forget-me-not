from api.controllers.users.controller import UserController
from api.docs.models import EndpointDict
from api.models.users.errors import LoggedOut, UserNotFoundError
from api.models.users.responses import UserResponse


class UserReadController(UserController):
    def run(self, user_id: int) -> UserResponse:
        self.user_id = user_id
        self.validate_access()
        model = self.repository.users.select_user(user_id)
        if model is None:
            raise UserNotFoundError
        return UserResponse.from_model(model)

    def validate_access(self):
        issuer = self.repository.users.select_user_by_token(
            self.ctx.get("token", "")
        )
        if issuer is None:
            raise LoggedOut

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="get /users/{user_id}",
            path={"user_id": "integer"},
            responses=UserResponse,
            errors=[UserNotFoundError, LoggedOut],
        )

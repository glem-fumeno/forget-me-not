from api.docs.models import EndpointDict
from api.users.controllers.core import UserController
from api.users.schemas.errors import LoggedOut
from api.users.schemas.responses import UserResponse


class UserReadMeController(UserController):
    def run(self) -> UserResponse:
        self.token = self.ctx.get("token", "")
        model = self.repository.select_user_by_token(self.token)
        if model is None:
            raise LoggedOut
        return UserResponse.from_model(model)

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="get /users/me",
            responses=UserResponse,
            errors=[LoggedOut],
        )

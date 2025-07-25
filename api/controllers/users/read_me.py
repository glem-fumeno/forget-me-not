from api.controllers.users.controller import UserController
from api.docs.models import EndpointDict
from api.models.users.errors import LoggedOut
from api.models.users.responses import UserResponse


class UserReadMeController(UserController):
    def run(self) -> UserResponse:
        self.token = self.ctx.get("token", "")
        model = self.repository.users.select_user_by_token(self.token)
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

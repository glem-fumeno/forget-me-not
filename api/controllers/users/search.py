from api.docs.models import EndpointDict
from api.controllers.users.core import UserController
from api.models.users.errors import LoggedOut
from api.models.users.responses import UserListResponse, UserResponse


class UserSearchController(UserController):
    def run(self) -> UserListResponse:
        self.validate_access()
        users = self.repository.select_users()
        return UserListResponse(
            users=[UserResponse.from_model(model) for model in users.values()],
            count=len(users),
        )

    def validate_access(self):
        issuer = self.repository.select_user_by_token(
            self.ctx.get("token", "")
        )
        if issuer is None:
            raise LoggedOut

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="get /users/search",
            responses=UserListResponse,
            errors=[LoggedOut],
        )

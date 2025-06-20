from api.docs.models import EndpointDict
from api.users.controllers.core import UserController
from api.users.schemas.errors import UserNotFoundError
from api.users.schemas.responses import UserResponse


class UserDeleteController(UserController):
    def run(self, user_id: int) -> UserResponse:
        model = self.repository.select_user(user_id)
        if model is None:
            raise UserNotFoundError
        self.repository.delete_user(user_id)
        return UserResponse.from_model(model)

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="delete /users/{user_id}",
            path={"user_id": "integer"},
            responses=UserResponse,
            errors=[UserNotFoundError],
        )

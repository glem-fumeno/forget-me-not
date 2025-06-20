from api.users.controllers.core import UserController
from api.users.schemas.errors import UserNotFoundError
from api.users.schemas.responses import UserResponse


class UserReadController(UserController):
    def run(self, user_id: int) -> UserResponse:
        model = self.repository.select_user(user_id)
        if model is None:
            raise UserNotFoundError
        return UserResponse.from_model(model)

from api.controllers.users.controller import UserController
from api.docs.models import EndpointDict
from api.models.users.errors import (
    Inaccessible,
    LoggedOut,
    UserExistsError,
    UserNotFoundError,
)
from api.models.users.requests import UserUpdateRequest
from api.models.users.responses import UserResponse
from api.security import get_hash


class UserUpdateController(UserController):
    def run(self, user_id: int, request: UserUpdateRequest) -> UserResponse:
        self.user_id = user_id
        self.validate_access()
        self.request = request
        model = self.repository.users.select_user(user_id)
        if model is None:
            raise UserNotFoundError
        self.model = model
        self.update_email()
        self.update_username()
        self.update_password()

        self.repository.users.update_user(self.model)
        return UserResponse.from_model(self.model)

    def validate_access(self):
        issuer = self.repository.users.select_user_by_token(
            self.ctx.get("token", "")
        )
        if issuer is None:
            raise LoggedOut
        if issuer.user_id != self.user_id and issuer.role != "admin":
            raise Inaccessible

    def update_email(self):
        if self.request.email is None:
            return
        duplicate = self.repository.users.select_user_id_by_email(
            self.request.email
        )
        if duplicate is not None and duplicate != self.user_id:
            raise UserExistsError
        self.model.email = self.request.email

    def update_username(self):
        if self.request.username is None:
            return
        self.model.username = self.request.username

    def update_password(self):
        if self.request.password is None:
            return
        self.request.password = get_hash(self.request.password)
        self.model.password = self.request.password

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="patch /users/{user_id}",
            path={"user_id": "integer"},
            body=UserUpdateRequest,
            responses=UserResponse,
            errors=[
                LoggedOut,
                Inaccessible,
                UserNotFoundError,
                UserExistsError,
            ],
        )

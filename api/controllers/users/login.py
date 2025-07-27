from api.controllers.users.controller import UserController
from api.docs.models import EndpointDict
from api.models.users.errors import InvalidCredentialsError
from api.models.users.requests import UserLoginRequest
from api.models.users.responses import UserTokenResponse
from api.security import get_hash, get_uuid


class UserLoginController(UserController):
    def run(self, request: UserLoginRequest) -> UserTokenResponse:
        request = request.model_copy()
        request.password = get_hash(request.password)
        user_id = self.repository.users.select_user_id_by_email(request.email)
        if user_id is None:
            raise InvalidCredentialsError
        model = self.repository.users.select_user(user_id)
        assert model is not None
        if model.password != request.password:
            raise InvalidCredentialsError
        token = get_uuid()
        self.repository.users.insert_user_session(user_id, token)
        return UserTokenResponse.from_model(model, token)

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="post /users/login",
            body=UserLoginRequest,
            responses=UserTokenResponse,
            errors=[InvalidCredentialsError],
        )

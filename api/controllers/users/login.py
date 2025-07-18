from api.controllers.users.controller import UserController
from api.docs.models import EndpointDict
from api.models.users.errors import InvalidCredentialsError
from api.models.users.models import UserSessionModel
from api.models.users.requests import UserLoginRequest
from api.models.users.responses import UserTokenResponse
from api.security import get_hash, get_uuid


class UserLoginController(UserController):
    def run(self, request: UserLoginRequest) -> UserTokenResponse:
        request.password = get_hash(request.password)
        user_id = self.repository.select_user_id_by_email(request.email)
        if user_id is None:
            raise InvalidCredentialsError
        model = self.repository.select_user(user_id)
        assert model is not None
        if model.password != request.password:
            raise InvalidCredentialsError
        session = UserSessionModel(user_id=user_id, token=get_uuid())
        self.repository.insert_user_session(session)
        return UserTokenResponse.from_model(model, session.token)

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="post /users/login",
            body=UserLoginRequest,
            responses=UserTokenResponse,
            errors=[InvalidCredentialsError],
        )

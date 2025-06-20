from api.users.common import get_hash, get_uuid
from api.users.controllers.core import UserController
from api.users.schemas.errors import InvalidCredentialsError
from api.users.schemas.models import UserSessionModel
from api.users.schemas.requests import UserLoginRequest
from api.users.schemas.responses import UserTokenResponse


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
        session = UserSessionModel(user_id, get_uuid())
        self.repository.insert_user_session(session)
        return UserTokenResponse.from_model(model, session.token)

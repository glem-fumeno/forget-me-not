from api.docs.models import EndpointDict
from api.users.common import get_hash, get_uuid
from api.users.controllers.core import UserController
from api.users.schemas.errors import UserExistsError
from api.users.schemas.models import UserSessionModel
from api.users.schemas.requests import UserLoginRequest
from api.users.schemas.responses import UserTokenResponse


class UserRegisterController(UserController):
    def run(self, request: UserLoginRequest) -> UserTokenResponse:
        request.password = get_hash(request.password)
        duplicate = self.repository.select_user_id_by_email(request.email)
        if duplicate is not None:
            raise UserExistsError
        model = request.to_model()
        self.repository.insert_user(model)
        session = UserSessionModel(user_id=model.user_id, token=get_uuid())
        self.repository.insert_user_session(session)
        return UserTokenResponse.from_model(model, session.token)

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="post /users/register",
            body=UserLoginRequest,
            responses=UserTokenResponse,
            errors=[UserExistsError],
        )

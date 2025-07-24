from api.controllers.users.controller import UserController
from api.docs.models import EndpointDict
from api.models.users.errors import UserExistsError
from api.models.users.models import UserSessionModel
from api.models.users.requests import UserLoginRequest
from api.models.users.responses import UserTokenResponse
from api.security import get_hash, get_uuid


class UserRegisterController(UserController):
    def run(self, request: UserLoginRequest) -> UserTokenResponse:
        request.password = get_hash(request.password)
        duplicate = self.repository.users.select_user_id_by_email(request.email)
        if duplicate is not None:
            raise UserExistsError
        model = request.to_model()
        users = self.repository.users.select_users()
        if len(users) < 1:
            model.role = "admin"
        self.repository.users.insert_user(model)
        session = UserSessionModel(user_id=model.user_id, token=get_uuid())
        self.repository.users.insert_user_session(session)
        return UserTokenResponse.from_model(model, session.token)

    @classmethod
    def get_docs(cls):
        return EndpointDict(
            endpoint="post /users/register",
            body=UserLoginRequest,
            responses=UserTokenResponse,
            errors=[UserExistsError],
        )

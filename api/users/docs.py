from api.docs.models import EndpointDict
from api.users.schemas.errors import InvalidCredentialsError, UserExistsError
from api.users.schemas.requests import UserLoginRequest
from api.users.schemas.responses import UserResponse, UserTokenResponse

endpoints: list[EndpointDict] = [
    EndpointDict(
        endpoint="post /users/login",
        body=UserLoginRequest,
        responses=UserTokenResponse,
        errors=[InvalidCredentialsError],
    ),
    EndpointDict(
        endpoint="post /users/register",
        body=UserLoginRequest,
        responses=UserTokenResponse,
        errors=[UserExistsError],
    ),
]

from api.docs.models import EndpointDict
from api.users.schemas.errors import InvalidCredentialsError
from api.users.schemas.requests import UserLoginRequest
from api.users.schemas.responses import UserResponse

endpoints: list[EndpointDict] = [
    EndpointDict(
        endpoint="post /users/login",
        body=UserLoginRequest,
        responses=UserResponse,
        errors=[InvalidCredentialsError],
    ),
]

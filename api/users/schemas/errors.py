from api.schemas import APIError


class InvalidCredentialsError(APIError):
    CODE = 401
    MESSAGE = "invalid credentials"

class UserExistsError(APIError):
    CODE = 409
    MESSAGE = "email already registered"

from api.schemas import Error


class InvalidCredentialsError(Error):
    CODE = 401
    MESSAGE = "invalid credentials"

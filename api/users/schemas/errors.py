from api.schemas import Error


class InvalidCredentialsError(Error):
    CODE = 401
    MESSAGE = "invalid credentials"

class UserExistsError(Error):
    CODE = 409
    MESSAGE = "email already registered"

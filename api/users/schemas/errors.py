from api.schemas import APIError


class InvalidCredentialsError(APIError):
    CODE = 401
    MESSAGE = "invalid credentials"

class UserExistsError(APIError):
    CODE = 409
    MESSAGE = "email already registered"

class UserNotFoundError(APIError):
    CODE = 404
    MESSAGE = "user not found"

class LoggedOut(APIError):
    CODE = 401
    MESSAGE = "logged out"

class Inaccessible(APIError):
    CODE = 403
    MESSAGE = "resource is inaccessible"

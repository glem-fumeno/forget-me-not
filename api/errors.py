class APIError(Exception):
    CODE = 500
    MESSAGE = "Internal Server Error"


class LoggedOut(APIError):
    CODE = 401
    MESSAGE = "logged out"


class Inaccessible(APIError):
    CODE = 403
    MESSAGE = "resource is inaccessible"

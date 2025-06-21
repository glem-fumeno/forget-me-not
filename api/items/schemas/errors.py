from api.errors import APIError


class ItemExistsError(APIError):
    CODE = 409
    MESSAGE = "item already exists"

class ItemNotFoundError(APIError):
    CODE = 404
    MESSAGE = "item not found"

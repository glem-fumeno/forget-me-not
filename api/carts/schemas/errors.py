from api.errors import APIError


class CartNotFoundError(APIError):
    CODE = 404
    MESSAGE = "cart not found"

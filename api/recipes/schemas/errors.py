from api.errors import APIError


class RecipeNotFoundError(APIError):
    CODE = 404
    MESSAGE = "recipe not found"


class ItemNotFoundError(APIError):
    CODE = 404
    MESSAGE = "item not found"

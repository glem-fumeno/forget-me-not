from api.errors import APIError


class RecipeNotFoundError(APIError):
    CODE = 404
    MESSAGE = "recipe not found"

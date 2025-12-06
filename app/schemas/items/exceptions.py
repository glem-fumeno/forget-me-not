from app.schemas.payload import APIException


class ItemAlreadyExists(APIException):
    CODE = 409
    DETAIL = "Item with this name already exists"


class ItemNotFound(APIException):
    CODE = 404
    DETAIL = "Item not found"

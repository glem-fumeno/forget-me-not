from dataclasses import dataclass
from typing import Self

from api.schemas import Response
from api.users.schemas.models import UserModel


@dataclass
class UserResponse(Response):
    user_id: int
    username: str
    email: str

    @classmethod
    def from_model(cls, model: UserModel) -> Self:
        return cls(model.user_id, model.username, model.email)

    @classmethod
    def get_example(cls) -> dict:
        return {
            "user_id": 15,
            "username": "alice",
            "email": "alice.johnson@example.com",
        }


@dataclass
class UserTokenResponse(Response):
    user_id: int
    username: str
    email: str
    token: str

    @classmethod
    def from_model(cls, model: UserModel, token: str) -> Self:
        return cls(model.user_id, model.username, model.email, token)

    @classmethod
    def get_example(cls) -> dict:
        return {
            "user_id": 15,
            "username": "alice",
            "email": "alice.johnson@example.com",
            "token": "983acfe0-0852-490c-8b92-7daf8c30d955",
        }

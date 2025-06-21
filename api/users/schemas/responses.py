from dataclasses import dataclass
from typing import Self

from api.schemas import Response
from api.users.schemas.models import RoleLiteral, UserModel


@dataclass
class UserResponse(Response):
    user_id: int
    username: str
    email: str
    role: RoleLiteral

    @classmethod
    def from_model(cls, model: UserModel) -> Self:
        return cls(model.user_id, model.username, model.email, model.role)

    @classmethod
    def get_example(cls) -> dict:
        return {
            "user_id": 15,
            "username": "alice",
            "email": "alice.johnson@example.com",
            "role": "admin",
        }


@dataclass
class UserTokenResponse(Response):
    user_id: int
    username: str
    email: str
    role: RoleLiteral
    token: str

    @classmethod
    def from_model(cls, model: UserModel, token: str) -> Self:
        return cls(
            model.user_id, model.username, model.email, model.role, token
        )

    @classmethod
    def get_example(cls) -> dict:
        return {
            "user_id": 15,
            "username": "alice",
            "email": "alice.johnson@example.com",
            "role": "admin",
            "token": "983acfe0-0852-490c-8b92-7daf8c30d955",
        }

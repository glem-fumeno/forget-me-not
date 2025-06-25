from typing import Self

from api.schemas import Response
from api.users.schemas.models import RoleLiteral, UserModel


class UserResponse(Response):
    user_id: int
    username: str
    email: str
    role: RoleLiteral

    @classmethod
    def from_model(cls, model: UserModel) -> Self:
        return cls(
            user_id=model.user_id,
            username=model.username,
            email=model.email,
            role=model.role,
        )

    @classmethod
    def get_example(cls) -> dict:
        return {
            "user_id": 15,
            "username": "alice",
            "email": "alice.johnson@example.com",
            "role": "admin",
        }


class UserListResponse(Response):
    users: list[UserResponse]
    count: int

    @classmethod
    def get_example(cls) -> dict:
        return {
            "users": [
                {
                    "user_id": 15,
                    "username": "alice",
                    "email": "alice.johnson@example.com",
                    "role": "admin",
                },
                {
                    "user_id": 34,
                    "username": "bob",
                    "email": "bob.martin@example.com",
                    "role": "user",
                },
            ],
            "count": 2,
        }


class UserTokenResponse(Response):
    user_id: int
    username: str
    email: str
    role: RoleLiteral
    token: str

    @classmethod
    def from_model(cls, model: UserModel, token: str) -> Self:
        return cls(
            user_id=model.user_id,
            username=model.username,
            email=model.email,
            role=model.role,
            token=token,
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

from typing import Any

from api.models.users.models import UserModel
from api.schemas import Request


class UserLoginRequest(Request):
    email: str
    password: str

    def to_model(self) -> UserModel:
        return UserModel(
            user_id=-1,
            cart_id=None,
            username=self.email,
            email=self.email,
            password=self.password,
            role="new",
        )

    @classmethod
    def get_examples(cls) -> dict[str, Any]:
        return {
            "alice": {
                "email": "alice.johnson@example.com",
                "password": "Password1!",
            },
            "bob": {
                "email": "bob.martin@example.com",
                "password": "Password2!",
            },
            "charlie": {
                "email": "charlie.adams@example.com",
                "password": "Password3!",
            },
        }


class UserUpdateRequest(Request):
    username: str | None = None
    email: str | None = None
    password: str | None = None

    @classmethod
    def get_examples(cls) -> dict[str, Any]:
        return {
            "alice": {
                "username": "aanderson",
            },
            "bob": {
                "email": "bob.baker@example.com",
            },
            "charlie": {
                "password": "SunsetDrive@34",
            },
        }

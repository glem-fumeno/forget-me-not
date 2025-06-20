from dataclasses import dataclass
from typing import Any

from api.schemas import Request
from api.users.schemas.models import UserModel


@dataclass
class UserLoginRequest(Request):
    email: str
    password: str

    def to_model(self) -> UserModel:
        return UserModel(0, self.email, self.email, self.password, "new")

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
            }
        }

@dataclass
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
            }
        }

from dataclasses import dataclass
from typing import Any

from api.schemas import Request


@dataclass
class UserLoginRequest(Request):
    email: str
    password: str

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

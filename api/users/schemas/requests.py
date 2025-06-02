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
            "default": {
                "email": "alice.johnson@example.com",
                "password": "Password1!",
            }
        }

from dataclasses import dataclass
from typing import Any

from api.schemas import Response


@dataclass
class UserResponse(Response):
    user_id: int
    username: str
    email: str

    @classmethod
    def get_example(cls) -> Any:
        return {
            "user_id": 15,
            "username": "alice",
            "email": "alice.johnson@example.com",
        }

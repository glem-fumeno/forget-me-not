from dataclasses import dataclass

from api.schemas import Model


@dataclass
class UserModel(Model):
    user_id: int
    username: str
    email: str
    password: str

@dataclass
class UserSessionModel(Model):
    user_id: int
    token: str

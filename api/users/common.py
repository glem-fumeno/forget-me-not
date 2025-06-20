import uuid
from hashlib import sha256

from config import CONFIG


def get_hash(value: str) -> str:
    return sha256((value + CONFIG["SALT"]).encode()).hexdigest()


def get_uuid() -> str:
    return uuid.uuid4().hex

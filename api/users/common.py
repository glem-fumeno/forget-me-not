import uuid
from hashlib import sha256

from config import get_config

config = get_config()


def get_hash(value: str) -> str:
    return sha256((value + config.SALT).encode()).hexdigest()


def get_uuid() -> str:
    return uuid.uuid4().hex

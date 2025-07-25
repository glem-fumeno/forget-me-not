import logging

import uvicorn

from config import get_config

config = get_config()


if __name__ == "__main__":
    uvicorn.run(
        "main:asgi",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEV_MODE,
        ssl_keyfile=config.SSL_KEY_PATH,
        ssl_certfile=config.SSL_CRT_PATH,
        log_level=logging.CRITICAL,
    )

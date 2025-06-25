#
#  szs-backend
#
#  Copyright 2024-2025 Elmark Automatyka S.A.
#

from __future__ import annotations

import sys

import loguru

from config import get_config

config = get_config()


def init_logger() -> None:
    loguru.logger.remove(0)
    loguru.logger.configure(extra={"hash": "00000000"})
    loguru.logger.add(
        sys.stdout,
        level=config.LOG_LEVEL,
        colorize=True,
        format=""
        "<lw>{extra[hash]} {file.path}:{line}</lw>\n"
        "<level>{level}</level> : {message}",
    )
    if config.LOG_FILE == "":
        return
    loguru.logger.add(config.LOG_FILE, level="DEBUG", serialize=True)

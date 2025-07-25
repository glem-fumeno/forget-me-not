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


def formatter(record):
    message = record["message"]
    level = record["level"].name
    if level == "INFO":
        level = f"<g><b>{level}</b></g>"
    else:
        level = f"<level>{level}</level>"
    return (
        f"<lw>{record['extra']['hash']} {record['file'].path}:{record['line']}</lw>\n"
        f"{level} : {message}\n"
    )


def init_logger() -> None:
    loguru.logger.remove(0)
    loguru.logger.configure(extra={"hash": "00000000"})
    loguru.logger.add(
        sys.stdout, level=config.LOG_LEVEL, colorize=True, format=formatter
    )
    if config.LOG_FILE == "":
        return
    loguru.logger.add(config.LOG_FILE, level="DEBUG", serialize=True)

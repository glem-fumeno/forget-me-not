import re
import sys

import loguru
import traceback_with_variables as twv

files = re.compile(r"/app/app")

twv.fmt.max_value_str_len = 80
twv.fmt.skip_files_except = [files]
twv.fmt.color_scheme = twv.ColorSchemes.common


global_format = (
    "<lw>{file.path}:{line} {extra[hash]}</lw>\n"
    "<level>{level}</level> : {message}"
)


def formatter(record):
    format = global_format + "\n"
    if not record["exception"]:
        return format
    exc_type, exc_value, tb = record["exception"]
    try:
        raise exc_type(exc_value).with_traceback(tb)
    except Exception as e:
        try:
            twv.print_exc(e, 1)
        except Exception:
            print(f"\n{e.__class__.__name__} {', '.join(map(str, e.args))}")
    return format


def init_logger() -> None:
    loguru.logger.remove(0)
    loguru.logger.configure(extra={"hash": "00000000"})
    loguru.logger.add(
        sys.stdout,
        level="INFO",
        colorize=True,
        backtrace=False,
        format=formatter,
    )

# -*- coding: utf-8 -*-
############################################################
#
# loguru guide, using logging.config
# https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.configure
############################################################

import sys

from loguru import logger

logger.configure(
    handlers=[
        dict(
            sink=sys.stderr,
            backtrace=False,
            filter=lambda record: "default" in record["extra"],
        ),
        dict(
            sink="log/default.log",
            backtrace=False,
            filter=lambda record: "default" in record["extra"],
        ),
        dict(
            sink=sys.stdout,
            backtrace=False,
            format="{message}",
            level="INFO",
            filter=lambda record: "emitter" in record["extra"],
        ),
        dict(
            sink="log/{time:YYYY-MM-DD}.log",
            filter=lambda record: "default" in record["extra"],
            backtrace=False,
            enqueue=True,
            rotation="10 MB",
        ),
    ]
)

statis_logger = logger.bind(emitter=True)
default_logger = logger.bind(default=True)


def init_logger(name, level):
    """Initialize logger in subprocess"""
    logger.add(
        sink=f"log/{name}-{level}.log",
        level=level,
        backtrace=False,
        rotation="1 day",
        retention="7 days",
        enqueue=True,
    )


loggers = {}


def get_a_single_logger(name, level):
    """Create a wrapper logger with extra info
    利用 filter 机制让这个 logger 的消息只输出到当前 sink 上
    """
    logger_key = f"{name}-{level}"
    if logger_key in loggers:
        return loggers.get(logger_key)

    logger.add(
        sink=f"log/{logger_key}.log",
        level=level,
        filter=lambda record: record["extra"].get("name") == name,
        backtrace=False,
        rotation="1 day",
        retention="7 days",
        enqueue=True,
    )
    # https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.bind
    wrapper_log = logger.bind(name=name)
    loggers[logger_key] = wrapper_log
    return wrapper_log

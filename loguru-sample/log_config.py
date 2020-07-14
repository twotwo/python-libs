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
        dict(sink=sys.stderr, backtrace=False,
             filter=lambda record: "default" in record["extra"]),
        dict(sink=sys.stdout, backtrace=False,
             format="{message}", level="INFO",
             filter=lambda record: "emitter" in record["extra"]),
        dict(sink="log/{time:YYYY-MM-DD}.log",
             filter=lambda record: "default" in record["extra"],
             backtrace=False, enqueue=True, rotation="10 MB"),
    ]
)

statis_logger = logger.bind(emitter=True)
default_logger = logger.bind(default=True)


def init_logger(name, level):
    logger.add(sink=f"log/{name}-{level}.log",
               level=level,
               backtrace=False,
               rotation="1 day",
               retention="7 days",
               enqueue=True,
               )
    return logger

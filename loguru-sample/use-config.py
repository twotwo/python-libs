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
             filter=lambda record: "defaut" in record["extra"]),
        dict(sink=sys.stdout, backtrace=False,
             format="{message}", level="INFO",
             filter=lambda record: "emitter" in record["extra"]),
        dict(sink="log/{time:YYYY-MM-DD}.log",
             filter=lambda record: "defaut" in record["extra"],
             backtrace=False, enqueue=True, rotation="10 MB"),
    ],
    patch=lambda record: record["extra"]
)

statis_logger = logger.bind(emitter=True)
default_logger = logger.bind(defaut=True)

default_logger.info('hello')

statis_logger.info('statis log')

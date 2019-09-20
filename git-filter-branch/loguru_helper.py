# -*- coding: utf-8 -*-
############################################################
#
# Replace logging with logura
#
############################################################
import sys
from loguru import logger

# https://loguru.readthedocs.io/en/stable/overview.html#suitable-for-scripts-and-libraries
# https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.configure
config = {
    "handlers": [
        # {"sink": sys.stdout, "format": "{time:YY-MM-DD HH:mm:ss} - {message}", "level": "DEBUG"},
        # {"sink": sys.stderr, "backtrace": False, "level": "INFO"},
    ]
}
logger.configure(**config)


# https://loguru.readthedocs.io/en/stable/resources/migration.html#replacing-logger-objects
# gethered messages to stdout; gether events to stderr
# pipe to supervisor
logger.add(sink=sys.stdout, format="{time:YY-MM-DD HH:mm:ss} - {message}",
           filter=lambda record: "stdout" in record["extra"])
message_logger = logger.bind(stdout=True)

logger.add(sink=sys.stderr, backtrace=False,
           filter=lambda record: "stderr" in record["extra"])
event_logger = logger.bind(stderr=True)

logger.add(sink=sys.stdout, format="{message}",
           filter=lambda record: "emitter" in record["extra"])
emit_logger = logger.bind(emitter=True)


if __name__ == '__main__':
    message_logger.info('stdout info')
    event_logger.info('event log: info')
    event_logger.error('event log: error')

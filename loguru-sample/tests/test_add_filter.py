import pytest
from loguru import logger


@pytest.mark.parametrize(
    "filter",
    [
        None,
        "",
        (lambda r: True),
        (lambda r: r["level"].name == "DEBUG"),
        {},
        {"": "DEBUG"},
        {"tests": True},
        {"tests.test_add_filter": 5, "tests": False},
        {"tests.test_add_filter.foobar": False},
        {"tests.": False},
        {"tests.test_add_filter.": False},
    ],
)
def test_filterd_in(filter, writer):
    logger.add(writer, filter=filter, format="{message}")
    logger.debug("Test Filter")
    assert writer.read() == "Test Filter\n"


def test_filter_as_function(writer):
    def error_filter(record):
        # "level": RecordLevel
        return record["level"].name == "ERROR" and "console" not in record["extra"]

    logger.add(writer, filter=error_filter, format="{message}")
    logger.debug("Debug Info")
    logger.error("Error Info")
    assert writer.read() == "Error Info\n"

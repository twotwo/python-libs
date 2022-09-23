import pytest

from loguru import logger

log_info = "Test level"


@pytest.mark.parametrize("level", [0, "TRACE", "INFO", 20])
def test_level_low_enough(writer, level):
    logger.add(writer, level=level, format="{message}")
    logger.info(log_info)
    assert writer.read() == "Test level\n"


@pytest.mark.parametrize("level", ["WARNING", 25])
def test_level_too_high(writer, level):
    logger.add(writer, level=level, format="{message}")
    logger.info(log_info)
    assert writer.read() == ""


def test_exception_on_error(writer):
    logger.add(
        writer, level="ERROR", format="{message}"
    )  # {level} {level.no} {level.name}
    logger.exception(log_info)
    assert writer.read().startswith(log_info)


@pytest.mark.parametrize("level", [3.4, object()])
def test_invalid_level(writer, level):
    with pytest.raises(TypeError):
        logger.add(writer, level=level)


@pytest.mark.parametrize("level", ["foo", -1])
def test_unknown_level(writer, level):
    with pytest.raises(ValueError):
        logger.add(writer, level=level)

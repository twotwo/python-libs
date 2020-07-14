from loguru import logger
import multiprocessing as mp
from log_config import init_logger


def test_basic_usage():
    """Basic Usage

    log to default handler
    add/remove handler
    """
    print()
    logger.info("with default handler")
    sink_id = logger.add("log/runtime.log", rotation="1 day")
    logger.info("add a file handler")
    logger.remove(sink_id)
    logger.info("remove file handler")


def test_rotation():
    pass


def create_process(name, level):
    init_logger(name, level)
    logger.info(f"{name} starting, process={mp.current_process().pid}")

    logger.info(f"{name} finished.")
    logger.remove()


def test_per_process_per_log():
    ctx = mp.get_context("spawn")

    processes = [
        ctx.Process(
            target=create_process,
            args=(
                f"proc_{i}",
                "DEBUG",
            ),
        )
        for i in range(10)
    ]
    for proc in processes:
        proc.start()


def test_config():
    from log_config import default_logger
    default_logger.info("hello")

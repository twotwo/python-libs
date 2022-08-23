import multiprocessing as mp

from loguru import logger

from log_config import default_logger, get_a_single_logger, init_logger


def test_basic_usage():
    """Basic Usage

    log to default handler
    add/remove handler
    """
    print()
    default_logger.info("with default handler")
    sink_id = logger.add("log/runtime.log", rotation="1 day")
    logger.info("add a file handler")
    logger.remove(sink_id)
    logger.info("remove file handler")


def test_one_sink_to_one_logger():
    my_logger = get_a_single_logger("boss", "INFO")
    logger.info("default handler")
    my_logger.info("boss log")


def create_process(name, level):
    # add handler in process
    init_logger(name, level)
    logger.info(f"{name} starting, process={mp.current_process().pid}")

    logger.info(f"{name} finished.")
    # Wait for the end of enqueued messages
    # and asynchronous tasks scheduled by handlers.
    logger.complete()


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

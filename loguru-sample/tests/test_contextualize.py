import threading

from loguru import logger


def test_contextualize(writer):
    logger.add(writer, format="{message} {extra[foo]} {extra[baz]}")

    with logger.contextualize(foo="bar", baz=123):
        logger.info("Contextualized")

    assert writer.read() == "Contextualized bar 123\n"


def test_contextualize_in_error(writer):
    logger.add(writer, format="{extra} {message}")

    with logger.contextualize(foo="bar", baz=123):
        logger.error("Contextualized")
        logger.error(RuntimeError("Something wrong"))

    assert (
        writer.read()
        == "{'foo': 'bar', 'baz': 123} Contextualized\n{'foo': 'bar', 'baz': 123} Something wrong\n"
    )


def test_contextualize_in_exception(writer):
    logger.add(writer, format="{extra} {message}")

    with logger.contextualize(foo="bar", baz=123):
        try:
            4 / 0
        except ZeroDivisionError:
            logger.exception("")
        print(writer.read())
        assert writer.read().startswith("{'foo': 'bar', 'baz': 123}")
        assert writer.read().endswith("ZeroDivisionError: division by zero\n")


def test_contextualize_as_decorator(writer):
    logger.add(writer, format="{message} {extra[foo]} {extra[baz]}")

    @logger.contextualize(foo=123, baz="bar")
    def task():
        logger.info("Contextualized")

    task()

    assert writer.read() == "Contextualized 123 bar\n"


def test_contextualize_in_function(writer):
    logger.add(writer, format="{message} {extra}")

    def foobar():
        logger.info("Foobar!")

    with logger.contextualize(foobar="baz"):
        foobar()

    assert writer.read() == "Foobar! {'foobar': 'baz'}\n"


def test_contextualize_thread(writer):
    logger.add(writer, format="{message} {extra[i]}")

    def task():
        logger.info("Processing")

    def create_worker(entry_barrier, exit_barrier, i):
        with logger.contextualize(i=i):
            entry_barrier.wait()
            task()
            exit_barrier.wait()

    entry_barrier = threading.Barrier(5)
    exit_barrier = threading.Barrier(5)

    threads = [
        threading.Thread(target=create_worker, args=(entry_barrier, exit_barrier, i))
        for i in range(5)
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    assert sorted(writer.read().splitlines()) == ["Processing %d" % i for i in range(5)]

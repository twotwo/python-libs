# https://github.com/Pegase745/sqlalchemy-datatables/blob/master/tests/conftest.py
from __future__ import print_function

import itertools

import pytest
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sample.domain import Base
from sample.repo.book import add_new_book

# from datetime import datetime, timedelta


# from sample.models import author_publisher, book_publisher
# from sample.models.auther import Author


def pytest_addoption(parser):
    parser.addoption(
        "--dburl",
        action="store",
        default="sqlite://",
        help="url of the database to use for tests",
    )

    parser.addoption(
        "--echo", action="store", default=False, help="engine echo param: True or False"
    )


def populate(session):
    """Create 3 publishers and 50 books."""

    f = Faker(locale="zh_CN", seed=1)
    publishers = ["人民邮电出版社", "电子工业出版社", "上海文艺出版社"]

    for i, p in zip(range(0, 50), itertools.cycle(publishers)):
        book = add_new_book(
            session, f"{f.first_name()} {f.last_name()}", f.company_prefix(), p
        )
        if 0:
            print(f"{i}, {book}")


@pytest.fixture(scope="session")
def engine(request):
    """
    https://docs.sqlalchemy.org/en/13/core/engines.html#sqlite

    dialect+driver://username:password@host:port/database
    """
    # SQLite :memory: database or file-based db
    db_url = request.config.getoption("--dburl")
    if str(db_url).find("sqlite://") != 0:
        db_url = f"sqlite:///{db_url}"
    echo = bool(request.config.getoption("--echo"))
    print(f"db_url={db_url}, echo={echo}")
    return create_engine(db_url, echo=echo)


@pytest.fixture(scope="session")
def session(engine):
    sessionmaker_ = sessionmaker(bind=engine)
    session = sessionmaker_()
    Base.metadata.create_all(engine)
    populate(session)

    yield session

    session.close()

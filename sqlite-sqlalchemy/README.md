# SQLAlchemy & Alembic with SQLite

This project was built using Python 3.7+

- [Code: data & function](https://realpython.com/python-sqlite-sqlalchemy/#using-sqlite-to-persist-data)
- [分层设计](https://www.oreilly.com/library/view/architecture-patterns-with/9781492052197/ch04.html) domain/repo
- [conftest.py](https://github.com/Pegase745/sqlalchemy-datatables)

## Python Virtualenv

I use the `pyenv` tool to install Python versions on my Mac. I find it a very useful tool, and the instructions that follow use it, and are based on having Python version 3.8.0 installed using the following command:

```shell
$ virtualenv venv -p python3 && \
    source venv/bin/activate && \
    pip install --upgrade pip
$ pip install -r requirements.txt && \
    pip install -r requirements-dev.txt
```

## Installing The Project

From the main folder take the following steps (on a Mac):

* Activate the virtual environment
  * ```source venv/bin/activate```
* Install the project:
  * `pip install -r requirements.txt`
* Reference
  * <https://docs.python.org/zh-cn/3.7/distutils/examples.html>

## Alembic Tutorial

[](https://alembic.sqlalchemy.org/en/latest/tutorial.html)

* Initial alembic environment
  * `venv/bin/alembic init sample/alembic`
  * `alembic.ini` created at local path
* Editing the .ini File
  * `sqlalchemy.url=sqlite:///sample/data/sample.db`
  * <https://docs.sqlalchemy.org/en/14/dialects/sqlite.html#dialect-sqlite-pysqlite-connect>
* Create a migration script
  * `alembic revision -m "init schema"`
  * `code sample/alembic/versions/2d157466a031_init_schema.py`
* Running our first migration
  * `alembic upgrade head`
* Getting Information
  * `alembic current`
  * `alembic history --verbose`
* Running our first migration
  * `alembic downgrade base`

## Learn by Unit Test

* Setup Python Path
  * `export PYTHONPATH=.`
* Test DB in Memory Mode
  * `pytest`
  * `pytest -s`
* Test DB in File Mode
  * `pytest -s --dburl=/tmp/s.db`
  * `sqlite3 /tmp/s.db`

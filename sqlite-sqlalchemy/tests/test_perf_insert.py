# Inserting 100,000 rows to SQLite3
import time
import sqlite3

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()
DBSession = scoped_session(sessionmaker())
engine = None


class Customer(Base):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))


def init_sqlalchemy(engine):
    DBSession.remove()
    DBSession.configure(bind=engine, autoflush=False, expire_on_commit=False)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def test_sqlalchemy_orm(engine, n=100000):
    init_sqlalchemy(engine)
    t0 = time.time()
    for i in range(n):
        customer = Customer()
        customer.name = "NAME " + str(i)
        DBSession.add(customer)
        if i % 1000 == 0:
            DBSession.flush()
    DBSession.commit()
    print(f"SQLAlchemy ORM: Total time for {n} records {time.time() - t0} secs")


def test_sqlalchemy_orm_pk_given(engine, n=100000):
    init_sqlalchemy(engine)
    t0 = time.time()
    for i in range(n):
        customer = Customer(id=i + 1, name="NAME " + str(i))
        DBSession.add(customer)
        if i % 1000 == 0:
            DBSession.flush()
    DBSession.commit()
    print(
        f"SQLAlchemy ORM pk given: Total time for {n} records {time.time() - t0} secs"
    )


def test_sqlalchemy_orm_bulk_save_objects(engine, n=100000):
    init_sqlalchemy(engine)
    t0 = time.time()
    for chunk in range(0, n, 10000):
        DBSession.bulk_save_objects(
            [
                Customer(name="NAME " + str(i))
                for i in range(chunk, min(chunk + 10000, n))
            ]
        )
    DBSession.commit()
    print(
        f"SQLAlchemy ORM bulk_save_objects(): Total time for {n} records {time.time() - t0} secs"
    )


def test_sqlalchemy_orm_bulk_insert(engine, n=100000):
    init_sqlalchemy(engine)
    t0 = time.time()
    for chunk in range(0, n, 10000):
        DBSession.bulk_insert_mappings(
            Customer,
            [dict(name="NAME " + str(i)) for i in range(chunk, min(chunk + 10000, n))],
        )
    DBSession.commit()
    print(
        f"SQLAlchemy ORM bulk_insert_mappings(): Total time for {n} records {time.time() - t0} secs"
    )


def test_sqlalchemy_core(engine, n=100000):
    init_sqlalchemy(engine)
    t0 = time.time()
    engine.execute(
        Customer.__table__.insert(), [{"name": "NAME " + str(i)} for i in range(n)]
    )
    print(f"SQLAlchemy Core: Total time for {n} records {time.time() - t0} secs")


def init_sqlite3(dbname):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS customer")
    c.execute(
        "CREATE TABLE customer (id INTEGER NOT NULL, "
        "name VARCHAR(255), PRIMARY KEY(id))"
    )
    conn.commit()
    return conn


def test_sqlite3(n=100000, dbname=":memory:"):
    conn = init_sqlite3(dbname)
    c = conn.cursor()
    t0 = time.time()
    for i in range(n):
        row = ("NAME " + str(i),)
        c.execute("INSERT INTO customer (name) VALUES (?)", row)
    conn.commit()
    print(f"sqlite3: Total time for {n} records {time.time() - t0} secs")

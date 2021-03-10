# https://github.com/sqlalchemy/sqlalchemy/blob/rel_1_3_23/test/perf/orm2010.py
from decimal import Decimal
import os
import random
import warnings

from sqlalchemy import __version__
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session


warnings.filterwarnings("ignore", r".*Decimal objects natively")  # noqa

# speed up cdecimal if available
try:
    import cdecimal
    import sys

    sys.modules["decimal"] = cdecimal
except ImportError:
    pass


Base = declarative_base()


class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)
    # 指定当存在继承类时，用于确定传入行的目标类的列、属性或SQL表达式
    __mapper_args__ = {"polymorphic_on": type}


class Boss(Employee):
    __tablename__ = "boss"

    id = Column(Integer, ForeignKey("employee.id"), primary_key=True)
    golf_average = Column(Numeric)
    # 指定由引用的列表达式返回的标识此特定类的值
    # polymorphic_on 设置。当收到行时，对应于 polymorphic_on 将列表达式与该值进行比较，指示应为新重建的对象使用哪个子类
    __mapper_args__ = {"polymorphic_identity": "boss"}


class Worker(Employee):
    __tablename__ = "worker"

    id = Column(Integer, ForeignKey("employee.id"), primary_key=True)
    savings = Column(Numeric)

    employer_id = Column(Integer, ForeignKey("boss.id"))

    employer = relationship(
        "Boss", backref="employees", primaryjoin=Boss.id == employer_id
    )

    __mapper_args__ = {"polymorphic_identity": "worker"}


######################################################################
# sqlite> .tables
# boss      employee  worker

# sqlite> .schema boss
# CREATE TABLE boss (
# 	id INTEGER NOT NULL,
# 	golf_average NUMERIC,
# 	PRIMARY KEY (id),
# 	FOREIGN KEY(id) REFERENCES employee (id)
# );
# sqlite> .schema employee
# CREATE TABLE employee (
# 	id INTEGER NOT NULL,
# 	name VARCHAR(100) NOT NULL,
# 	type VARCHAR(50) NOT NULL,
# 	PRIMARY KEY (id)
# );
# sqlite> .schema worker
# CREATE TABLE worker (
# 	id INTEGER NOT NULL,
# 	savings NUMERIC,
# 	employer_id INTEGER,
# 	PRIMARY KEY (id),
# 	FOREIGN KEY(id) REFERENCES employee (id),
# 	FOREIGN KEY(employer_id) REFERENCES boss (id)
# );
######################################################################

# in-memory database
engine = create_engine("sqlite://")

Base.metadata.create_all(engine)

sess = Session(engine)


def runit(status, factor=1, query_runs=5):
    num_bosses = 100 * factor
    num_workers = num_bosses * 100

    bosses = [
        Boss(name="Boss %d" % i, golf_average=Decimal(random.randint(40, 150)))
        for i in range(num_bosses)
    ]

    sess.add_all(bosses)
    status(f"Added {num_bosses} boss objects")

    workers = [
        Worker(
            name="Worker %d" % i,
            savings=Decimal(random.randint(5000000, 15000000) / 100),
        )
        for i in range(num_workers)
    ]
    status(f"Added {num_workers} worker objects")

    while workers:
        # this doesn't associate workers with bosses evenly,
        # just associates lots of them with a relatively small
        # handful of bosses
        batch_size = 100
        batch_num = (num_workers - len(workers)) / batch_size
        boss = sess.query(Boss).filter_by(name="Boss %d" % batch_num).first()
        for worker in workers[0:batch_size]:
            worker.employer = boss

        workers = workers[batch_size:]

    sess.commit()
    status("Associated workers w/ bosses and committed")

    # do some heavier reading
    for i in range(query_runs):
        status("Heavy query run #%d" % (i + 1))

        report = []

        # load all the Workers, print a report with their name, stats,
        # and their bosses' stats.
        for worker in sess.query(Worker):
            report.append(
                (
                    worker.name,
                    worker.savings,
                    worker.employer.name,
                    worker.employer.golf_average,
                )
            )

        sess.close()  # close out the session


def run_with_profile(runsnake=False, dump=False):
    import cProfile
    import pstats

    filename = "orm2010.profile"

    if os.path.exists("orm2010.profile"):
        os.remove("orm2010.profile")

    def status(msg):
        print(msg)

    cProfile.runctx("runit(status)", globals(), locals(), filename)
    stats = pstats.Stats(filename)

    counts_by_methname = dict((key[2], stats.stats[key][0]) for key in stats.stats)

    print("SQLA Version: %s" % __version__)
    print("Total calls %d" % stats.total_calls)
    print("Total cpu seconds: %.2f" % stats.total_tt)
    print(
        "Total execute calls: %d"
        % counts_by_methname["<method 'execute' of 'sqlite3.Cursor' " "objects>"]
    )
    print(
        "Total executemany calls: %d"
        % counts_by_methname.get(
            "<method 'executemany' of 'sqlite3.Cursor' " "objects>", 0
        )
    )

    if dump:
        stats.sort_stats("time", "calls")
        stats.print_stats()

    if runsnake:
        os.system("runsnake %s" % filename)


def run_with_time():
    import time

    now = time.time()

    def status(msg):
        print("%d - %s" % (time.time() - now, msg))

    runit(status, 10)
    print("Total time: %d" % (time.time() - now))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--profile",
        action="store_true",
        help="run shorter test suite w/ cprofilng",
    )
    parser.add_argument(
        "--dump",
        action="store_true",
        help="dump full call profile (implies --profile)",
    )
    parser.add_argument(
        "--runsnake",
        action="store_true",
        help="invoke runsnakerun (implies --profile)",
    )

    args = parser.parse_args()

    args.profile = args.profile or args.dump or args.runsnake

    if args.profile:
        run_with_profile(runsnake=args.runsnake, dump=args.dump)
    else:
        run_with_time()

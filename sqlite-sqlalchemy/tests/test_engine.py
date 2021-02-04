# 通过 Engine 连接入 SQLite，使用 DB-API 操作数据


def test_init_db(engine):
    engine.execute(
        """
            CREATE TABLE IF NOT EXISTS employee (
                emp_id integer primary key,
                emp_name varchar
            )
        """
        # https://www.sqlite.org/lang_createtable.html
        # https://sqlite.org/autoinc.html AUTOINCREMENT
    )
    # delete data
    engine.execute("""delete from employee""")
    # init data
    engine.execute("""insert into employee(emp_name) values ('ed')""")
    engine.execute("""insert into employee(emp_name) values ('jack')""")
    engine.execute("""insert into employee(emp_name) values ('fred')""")


def test_query_all(engine):
    print("=" * 100 + " test_query_all")
    result = engine.execute("select * from employee")
    for row in result:
        print(row)
    result.close()


def test_query_by_empid(engine):
    print("=" * 100 + " test_query_by_empid")
    result = engine.execute(
        "select emp_id, emp_name from " "employee where emp_id=:emp_id", emp_id=3
    )

    row = result.fetchone()
    print(row)
    print(row["emp_name"])
    result.close()

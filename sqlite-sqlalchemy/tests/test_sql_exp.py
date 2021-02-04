# 通过 SQL Expression 操作数据库

from sqlalchemy import Column, Integer, MetaData, String, Table

metadata = MetaData()
user_table = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("fullname", String),
)


def test_sql_expression():
    from sqlalchemy import and_, or_

    express_str = str(
        and_(
            user_table.c.fullname == "ed jones",
            or_(user_table.c.name == "ed", user_table.c.name == "jack"),
        )
    )
    expect = '"user".fullname = :fullname_1 AND ("user".name = :name_1 OR "user".name = :name_2)'

    assert expect == express_str


def test_comparison_operators():
    assert '"user".id > :id_1' == str(user_table.c.id > 5)

    assert '"user".name IS NULL' == str(user_table.c.name == None)

    assert '"user".id + :id_1' == str(user_table.c.id + 5)

    assert '"user".fullname || :fullname_1' == str(user_table.c.fullname + "some name")

    assert '"user".name IN (:name_1, :name_2, :name_3)' == str(
        user_table.c.name.in_(["wendy", "mary", "ed"])
    )


def test_dialect():
    """Expressions produce different strings according to *dialect* object"""
    expression = user_table.c.name == "ed"
    from sqlalchemy.dialects import mysql

    assert "user.name = %s" == str(expression.compile(dialect=mysql.dialect()))

    from sqlalchemy.dialects import postgresql

    assert '"user".name = %(name_1)s' == str(
        expression.compile(dialect=postgresql.dialect())
    )

    compiled = expression.compile()
    assert "{'name_1': 'ed'}" == str(compiled.params)


def test_execute(engine):
    # reset data for test
    metadata.drop_all(engine)
    metadata.create_all(engine)
    insert_stmt = user_table.insert().values(name="ed", fullname="Ed Jones")
    assert 'INSERT INTO "user" (name, fullname) VALUES (:name, :fullname)' == str(
        insert_stmt
    )
    result = engine.execute(insert_stmt)
    assert result.inserted_primary_key == [1]

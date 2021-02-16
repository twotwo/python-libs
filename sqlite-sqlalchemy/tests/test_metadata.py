# 通过 Metadata 操作数据库
# https://docs.sqlalchemy.org/en/13/core/metadata.html

from sqlalchemy import Column, Integer, MetaData, String, Table

metadata = MetaData()
# 表对象的 schema/types 由 MetaData/Table/Columns 等类型构成
user_table = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("fullname", String),
)


def test_metadata():
    assert "user" == user_table.name
    assert ["id", "name", "fullname"] == user_table.c.keys()
    assert ["id"] == user_table.primary_key.columns.keys()


def test_generate_schema(engine):
    """
    Table and MetaData objects can be used to generate a schema in database
    """
    metadata.create_all(engine)


def test_generate_another_schema(engine):
    """ForeignKey is used to link one column to a remote primary"""
    from sqlalchemy import ForeignKey

    addresses_table = Table(
        "address",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("email_address", String(100), nullable=False),
        Column("user_id", Integer, ForeignKey("user.id")),
    )

    if not addresses_table.exists(engine):
        addresses_table.create(engine)


def test_reflection(engine):
    metadata2 = MetaData()
    user_reflected = Table("user", metadata2, autoload=True, autoload_with=engine)
    assert ["id", "name", "fullname"] == user_reflected.c.keys()

    from sqlalchemy import inspect

    inspector = inspect(engine)
    assert ["address", "employee", "user"] == inspector.get_table_names()
    assert "id" == inspector.get_columns("address")[0]["name"]

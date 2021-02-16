# 通过 ORM 操作数据库

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    # a table should has a primary key
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    def __repr__(self):
        return "<User(%r, %r)>" % (self.name, self.fullname)


def test_inspect():
    from sqlalchemy import inspect

    mapper = inspect(User)
    # https://docs.sqlalchemy.org/en/13/orm/mapping_api.html#sqlalchemy.orm.Mapper.persist_selectable
    assert "user" == mapper.persist_selectable.name
    for column in mapper.columns:
        print(column)


def test_orm():
    assert "user" == str(User.__table__)
    # assert isinstance(User.__mapper__, User)
    assert "mapped class User->user" == str(User.__mapper__)
    ed_user = User(name="ed", fullname="Edward Jones")

    # The "id" field is the primary key, which starts as None
    assert ed_user.id is None


def test_session(engine, session):
    """use a Session object with orm"""
    Base.metadata.create_all(engine)
    ed_user = User(name="ed", fullname="Edward Jones")
    session.add(ed_user)
    # our_user = session.query(User).filter_by(name="ed").first()
    our_user = session.query(User).filter(User.name == "ed").first()
    assert our_user.id == 1

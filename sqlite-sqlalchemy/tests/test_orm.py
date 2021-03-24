# 通过 ORM 操作数据库：pytest --echo=true tests/test_orm.py -s
# https://docs.sqlalchemy.org/en/13/orm/tutorial.html
#
# https://docs.sqlalchemy.org/en/13/orm/session.html
# The mapper() function and declarative extensions are the primary configurational interface for the ORM.
# Once mappings are configured, the primary usage interface for persistence operations is the Session.


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


def test_query(session):
    from sqlalchemy import asc
    result = session.query(User.name, User.fullname).order_by(asc("fullname"))
    # https://docs.sqlalchemy.org/en/13/faq/sessions.html#query-has-no-len-why-not
    assert len(list(result)) == 1
    assert list(result)[0].name == "ed"
    assert list(result)[0].fullname == "Edward Jones"


# def test_get_books_by_publishers(session):
#     from sample.repo.book import get_books_by_publishers
#     books_by_publisher = get_books_by_publishers(session, ascending=False)
#     # https://docs.sqlalchemy.org/en/13/faq/sessions.html#query-has-no-len-why-not
#     assert len(list(books_by_publisher)) == 3

#     # for row in books_by_publisher:
#     #     print(f"Publisher: {row.name}, total books: {row.total_books}")
#     assert list(books_by_publisher)[0].total_books == 17

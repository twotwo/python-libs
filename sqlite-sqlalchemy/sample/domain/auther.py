# from datetime import datetime  # default=datetime.now
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref
from . import Base, ModelMixin, author_publisher


class Author(Base, ModelMixin):  # type: ignore
    __tablename__ = "author"
    author_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    books = relationship("Book", backref=backref("author"))
    publishers = relationship("Publisher",
                              secondary=author_publisher,
                              back_populates="authors")

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from . import Base, ModelMixin, author_publisher, book_publisher


class Publisher(Base, ModelMixin):
    __tablename__ = "publisher"
    publisher_id = Column(Integer, primary_key=True)
    name = Column(String)
    authors = relationship(
        "Author", secondary=author_publisher, back_populates="publishers"
    )
    books = relationship("Book", secondary=book_publisher, back_populates="publishers")

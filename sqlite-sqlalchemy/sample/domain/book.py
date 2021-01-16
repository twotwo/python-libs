# from datetime import datetime  # default=datetime.now
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import Base, ModelMixin, book_publisher


class Book(Base, ModelMixin):  # type: ignore
    __tablename__ = "book"
    book_id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("author.author_id"))
    title = Column(String)
    publishers = relationship("Publisher",
                              secondary=book_publisher,
                              back_populates="books")

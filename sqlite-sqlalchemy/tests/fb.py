"""
Defining factories with Factory Boy

https://factoryboy.readthedocs.io/en/stable/
"""
import factory

from sample.domain.book import Book


class BookFactory(factory.Factory):
    class Meta:
        model = Book

    title = factory.Faker("sentence", locale="zh_CN", nb_words=4)

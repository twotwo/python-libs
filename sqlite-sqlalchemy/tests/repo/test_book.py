from sample.repo.book import get_books_by_publishers, add_new_book
from tests.fb import BookFactory


def test_read(session):
    # Get the number of books printed by each publisher
    books_by_publisher = get_books_by_publishers(session, ascending=False)
    for row in books_by_publisher:
        print(f"Publisher: {row.name}, total books: {row.total_books}")
    print()


def test_book(session):
    # Returns a User instance that's not saved
    book = BookFactory.build()
    print(book)

from sqlalchemy import and_, asc, desc, func

from sample.domain.auther import Author
from sample.domain.book import Book
from sample.domain.publisher import Publisher


def get_books_by_publishers(session, ascending=True):
    """Get a list of publishers and the number of books they've published

    Args:
        session: database session to use
        ascending: direction to sort the results

    Returns:
        List: list of publisher sorted by number of books published
    """
    if not isinstance(ascending, bool):
        raise ValueError(f"Sorting value invalid: {ascending}")

    direction = asc if ascending else desc

    return (
        session.query(Publisher.name, func.count(Book.title).label("total_books"))
        .join(Publisher.books)
        .group_by(Publisher.name)
        .order_by(direction("total_books"))
    )


def add_new_book(session, author_name, book_title, publisher_name):
    """Adds a new book to the system"""

    # Get the author's first and last names
    first_name, _, last_name = author_name.partition(" ")

    book = Book(title=book_title)

    # Get the author
    author = (
        session.query(Author)
        .filter(and_(Author.first_name == first_name, Author.last_name == last_name))
        .one_or_none()
    )
    # Do we need to create the author?
    if author is None:
        author = Author(first_name=first_name, last_name=last_name)
        session.add(author)

    # Get the publisher
    publisher = (
        session.query(Publisher).filter(Publisher.name == publisher_name).one_or_none()
    )
    # Do we need to create the publisher?
    if publisher is None:
        publisher = Publisher(name=publisher_name)
        session.add(publisher)

    # Initialize the book relationships
    book.author = author
    book.publishers.append(publisher)
    session.add(book)

    # Commit to the database
    session.commit()
    return book

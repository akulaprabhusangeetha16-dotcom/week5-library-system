from library import Library
from book import Book
from member import Member


def test_add_book():
    library = Library()
    book = Book("Test Book", "Author", "12345", "2024")

    result = library.add_book(book)

    assert "successfully" in result.lower()


def test_register_member():
    library = Library()
    member = Member("Test User", "M999")

    result = library.register_member(member)

    assert "successfully" in result.lower()

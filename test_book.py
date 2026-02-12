from book import Book


def test_book_creation():
    book = Book("Test Title", "Author", "999", "2024")

    assert book.title == "Test Title"
    assert book.author == "Author"
    assert book.isbn == "999"
    assert book.available is True

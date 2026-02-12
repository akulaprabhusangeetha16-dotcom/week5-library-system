# member.py

class Member:
    """Represents a library member"""

    MAX_BORROW_LIMIT = 5   # Maximum books a member can borrow

    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []   # List of borrowed book ISBNs

    def borrow_book(self, isbn):
        """Add book to member's borrowed list"""
        if len(self.borrowed_books) >= self.MAX_BORROW_LIMIT:
            return False, "Borrow limit reached (5 books maximum)"

        if isbn in self.borrowed_books:
            return False, "Book already borrowed by this member"

        self.borrowed_books.append(isbn)
        return True, "Book added to member account"

    def return_book(self, isbn):
        """Remove book from borrowed list"""
        if isbn not in self.borrowed_books:
            return False, "This book was not borrowed by the member"

        self.borrowed_books.remove(isbn)
        return True, "Book removed from member account"

    def to_dict(self):
        """Convert object to dictionary (for JSON saving)"""
        return {
            "name": self.name,
            "member_id": self.member_id,
            "borrowed_books": self.borrowed_books
        }

    @classmethod
    def from_dict(cls, data):
        """Create Member object from dictionary"""
        member = cls(data["name"], data["member_id"])
        member.borrowed_books = data.get("borrowed_books", [])
        return member

    def __str__(self):
        return f"{self.name} (ID: {self.member_id}) - Borrowed: {len(self.borrowed_books)} books"

# book.py
from datetime import datetime, timedelta


class Book:
    """Represents a book in the library"""

    FINE_PER_DAY = 10  # ₹10 per day fine

    def __init__(self, title, author, isbn, year=None):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = year

        self.available = True
        self.borrowed_by = None
        self.borrow_date = None
        self.due_date = None
        self.date_added = datetime.now().strftime('%Y-%m-%d')

    def check_out(self, member_id, loan_days=14):
        if not self.available:
            return False, "Book is already borrowed"

        self.available = False
        self.borrowed_by = member_id
        self.borrow_date = datetime.now().strftime('%Y-%m-%d')
        self.due_date = (datetime.now() + timedelta(days=loan_days)).strftime('%Y-%m-%d')

        return True, f"Book borrowed successfully. Due date: {self.due_date}"

    def return_book(self):
        if self.available:
            return False, "Book is already available", None

        fine = self.calculate_fine()
        was_overdue = self.is_overdue()
        return_date = datetime.now().strftime('%Y-%m-%d')

        history_record = {
            "member_id": self.borrowed_by,
            "borrow_date": self.borrow_date,
            "return_date": return_date,
            "fine_paid": fine
        }

        self.available = True
        self.borrowed_by = None
        self.borrow_date = None
        self.due_date = None

        if was_overdue:
            return True, f"Book returned. Fine: ₹{fine}", history_record

        return True, "Book returned successfully", history_record

    def is_overdue(self):
        if self.due_date and not self.available:
            due = datetime.strptime(self.due_date, '%Y-%m-%d')
            return datetime.now() > due
        return False

    def days_overdue(self):
        if self.is_overdue():
            due = datetime.strptime(self.due_date, '%Y-%m-%d')
            return (datetime.now() - due).days
        return 0

    def calculate_fine(self):
        return self.days_overdue() * self.FINE_PER_DAY

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        book = cls(data['title'], data['author'], data['isbn'], data.get('year'))
        book.__dict__.update(data)
        return book

    def __str__(self):
        status = "Available" if self.available else f"Borrowed by {self.borrowed_by}"
        return f"{self.title} by {self.author} ({self.isbn}) - {status}"

# library.py

from database import connect


class Library:

    def add_book(self, book):
        conn = connect()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO books
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (book.isbn, book.title, book.author, book.year,
                  1, None, None, None))
            conn.commit()
            return "Book added successfully"
        except:
            return "Book already exists"
        finally:
            conn.close()

    def register_member(self, member):
        conn = connect()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO members VALUES (?, ?)
            """, (member.member_id, member.name))
            conn.commit()
            return "Member registered successfully"
        except:
            return "Member already exists"
        finally:
            conn.close()

    def borrow_book(self, member_id, isbn):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("SELECT available FROM books WHERE isbn=?", (isbn,))
        data = cursor.fetchone()

        if not data:
            conn.close()
            return "Book not found"

        if data[0] == 0:
            conn.close()
            return "Book already borrowed"

        cursor.execute("""
            UPDATE books
            SET available=0,
                borrowed_by=?,
                borrow_date=date('now'),
                due_date=date('now','+14 day')
            WHERE isbn=?
        """, (member_id, isbn))

        conn.commit()
        conn.close()
        return "Book borrowed successfully"

    def return_book(self, member_id, isbn):
        conn = connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT title, borrow_date FROM books WHERE isbn=?
        """, (isbn,))
        data = cursor.fetchone()

        if not data:
            conn.close()
            return "Book not found"

        title, borrow_date = data

        cursor.execute("""
            UPDATE books
            SET available=1,
                borrowed_by=NULL,
                borrow_date=NULL,
                due_date=NULL
            WHERE isbn=?
        """, (isbn,))

        cursor.execute("""
            INSERT INTO history
            (isbn, title, member_id, borrow_date, return_date, fine_paid)
            VALUES (?, ?, ?, ?, date('now'), 0)
        """, (isbn, title, member_id, borrow_date))

        conn.commit()
        conn.close()
        return "Book returned successfully"

    def view_books(self):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()
        conn.close()
        return books

    def view_history(self):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM history")
        history = cursor.fetchall()
        conn.close()
        return history
import shutil
import os
from datetime import datetime

def backup_database():
    if not os.path.exists("data/backup"):
        os.makedirs("data/backup")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"data/backup/library_backup_{timestamp}.db"

    shutil.copy("library.db", backup_name)

    return f"Backup created: {backup_name}"

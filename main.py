# main.py

from library import Library
from book import Book
from member import Member
from database import create_tables, connect
import hashlib


def login():
    conn = connect()
    cursor = conn.cursor()

    print("\n===== LOGIN =====")
    username = input("Username: ")
    password = input("Password: ")

    hashed = hashlib.sha256(password.encode()).hexdigest()

    cursor.execute("""
        SELECT role FROM admins
        WHERE username=? AND password=?
    """, (username, hashed))

    result = cursor.fetchone()
    conn.close()

    if result:
        print(f"Login successful! Role: {result[0].upper()}")
        return username, result[0]
    else:
        print("Invalid credentials!")
        return None, None


def change_password(username):
    conn = connect()
    cursor = conn.cursor()

    current = input("Current Password: ")
    new_pass = input("New Password: ")

    current_hash = hashlib.sha256(current.encode()).hexdigest()

    cursor.execute("""
        SELECT * FROM admins
        WHERE username=? AND password=?
    """, (username, current_hash))

    if not cursor.fetchone():
        print("Incorrect current password.")
        conn.close()
        return

    new_hash = hashlib.sha256(new_pass.encode()).hexdigest()

    cursor.execute("""
        UPDATE admins SET password=?
        WHERE username=?
    """, (new_hash, username))

    conn.commit()
    conn.close()
    print("Password changed successfully.")


def display_menu(role):
    print("\n===== LIBRARY SYSTEM =====")

    if role == "admin":
        print("1. Add Book")
        print("2. Register Member")

    print("3. Borrow Book")
    print("4. Return Book")
    print("5. View Books")

    if role == "admin":
        print("6. View History")

    print("7. Change Password")
    print("0. Exit")


def main():

    create_tables()

    username, role = login()
    if not role:
        return

    library = Library()

    while True:
        display_menu(role)
        choice = input("Enter choice: ")

        if choice == "1" and role == "admin":
            book = Book(
                input("Title: "),
                input("Author: "),
                input("ISBN: "),
                input("Year: ")
            )
            print(library.add_book(book))

        elif choice == "2" and role == "admin":
            member = Member(
                input("Member Name: "),
                input("Member ID: ")
            )
            print(library.register_member(member))

        elif choice == "3":
            print(library.borrow_book(
                input("Member ID: "),
                input("ISBN: ")
            ))

        elif choice == "4":
            print(library.return_book(
                input("Member ID: "),
                input("ISBN: ")
            ))

        elif choice == "5":
            books = library.view_books()
            for b in books:
                print("-" * 40)
                print(f"ISBN: {b[0]}")
                print(f"Title: {b[1]}")
                print(f"Author: {b[2]}")
                print(f"Available: {'Yes' if b[4] == 1 else 'No'}")

        elif choice == "6" and role == "admin":
            history = library.view_history()
            for h in history:
                print("-" * 40)
                print(f"ID: {h[0]}")
                print(f"Title: {h[2]}")
                print(f"Member: {h[3]}")
                print(f"Borrow: {h[4]}")
                print(f"Return: {h[5]}")

        elif choice == "7":
            change_password(username)

        elif choice == "0":
            print("Exiting system...")
            break

        else:
            print("Invalid option or permission denied.")


if __name__ == "__main__":
    main()

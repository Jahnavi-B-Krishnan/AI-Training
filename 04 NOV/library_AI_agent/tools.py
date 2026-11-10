
import json
import os

# Get the directory where this Python file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BOOKS_FILE = os.path.join(BASE_DIR, "books.json")
RESERVATIONS_FILE = os.path.join(BASE_DIR, "reservations.json")


# Read books from JSON
def load_books():
    with open(BOOKS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# Save updated books into JSON
def save_books(books):
    with open(BOOKS_FILE, "w", encoding="utf-8") as file:
        json.dump(books, file, indent=4)


# Read reservations from JSON
def load_reservations():
    with open(RESERVATIONS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# Save reservations into JSON
def save_reservations(reservations):
    with open(RESERVATIONS_FILE, "w", encoding="utf-8") as file:
        json.dump(reservations, file, indent=4)


# TOOL 1: Search books
def search_books(keyword):

    books = load_books()

    keyword = keyword.lower().strip()

    results = []

    for book in books:

        if (
            keyword in book["title"].lower()
            or keyword in book["author"].lower()
            or keyword in book["category"].lower()
        ):
            results.append({
                "id": book["id"],
                "title": book["title"],
                "author": book["author"],
                "category": book["category"],
                "available_copies": book["available_copies"]
            })

    if results:
        return {
            "status": "success",
            "results": results
        }

    return {
        "status": "not_found",
        "message": "No matching books found."
    }


# TOOL 2: Reserve a book
def reserve_book(book_id, customer_name):

    books = load_books()

    reservations = load_reservations()

    # Find the requested book
    selected_book = None

    for book in books:

        if book["id"] == book_id:
            selected_book = book
            break

    # Check if book exists
    if selected_book is None:
        return {
            "status": "error",
            "message": "Book ID not found."
        }

    # Check availability
    if selected_book["available_copies"] <= 0:
        return {
            "status": "unavailable",
            "message": f"{selected_book['title']} has no available copies."
        }

    # Ask user for confirmation
    print("\nReservation Confirmation")
    print("------------------------")
    print("Book:", selected_book["title"])
    print("Customer:", customer_name)

    confirmation = input(
        "Do you want to confirm this reservation? (yes/no): "
    ).strip().lower()

    if confirmation not in ["yes", "y"]:
        return {
            "status": "cancelled",
            "message": "Reservation was not created."
        }

    # Create reservation
    reservation = {
        "reservation_id": len(reservations) + 1,
        "book_id": book_id,
        "book_title": selected_book["title"],
        "customer_name": customer_name,
        "status": "Confirmed"
    }

    reservations.append(reservation)

    # Reduce available copies
    selected_book["available_copies"] -= 1

    # Save both JSON files
    save_reservations(reservations)
    save_books(books)

    return {
        "status": "success",
        "reservation": reservation,
        "remaining_copies": selected_book["available_copies"]
    }

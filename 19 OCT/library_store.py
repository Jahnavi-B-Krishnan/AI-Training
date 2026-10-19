from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2

app = FastAPI()

class Books (BaseModel):
    book_id: int
    title: str
    author: str
    category: str
    price: float
    stock: int
def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="library_store",
        user="postgres",
        password="Admin@123",
    )
    print("Connected to PostgreSQL successfully")
    return conn

# @app.get("/books")
# def get_books():
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM books")
#     rows = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return rows

@app.post("/books")
def add_book(book: Books):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO books (book_id, title, author, category, price, stock)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (book.book_id,book.title, book.author, book.category, book.price, book.stock)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {
        "message": "Book added successfully",
        "book": book
    }
# @app.get("/books")
# def get_books():
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM books WHERE category = 'Technology'")
#     rows = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return rows

# @app.get("/books")
# def get_books():
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM books WHERE price > 600")
#     rows = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return rows

from fastapi import HTTPException
@app.put("/books/{book_id}")
def update_book(book_id: int, book: Books):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE books
        SET title=%s, 
            author=%s, 
            category=%s, 
            price=%s, 
            stock=%s
        WHERE book_id=%s
        """,
        (book.title, book.author, book.category, book.price, book.stock,book_id)
    )
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Book updated successfully"}
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        DELETE FROM books WHERE book_id=%s
        """,
        (book_id,)
    )
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Book deleted successfully"}

# @app.get("/books")
# def get_books():
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM books WHERE price = (SELECT MAX(price) FROM books)")
#     rows = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return rows

# @app.get("/books")
# def get_books():
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT SUM(stock) AS Total_Stock FROM books")
#     rows = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return rows

@app.get("/books")
def get_books():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT category,SUM(stock) FROM books GROUP BY category")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


conn = get_connection()
conn.close()

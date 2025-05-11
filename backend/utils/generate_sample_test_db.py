import sqlite3
import os

# set database name
DB_NAME = 'books.db' # test

# connect to the database
def connect_db(db_name):
    return sqlite3.connect(db_name)

# create the books table if it doesn't exist
def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        cost REAL NOT NULL,
        genre TEXT NOT NULL,
        age_rating TEXT NOT NULL
    )
    ''')
    conn.commit()

# insert sample book data into the table
def insert_sample_data(conn):
    books_data = [
        ("The Great Gatsby", "F. Scott Fitzgerald", 10.99, "Classic", "13+"),
        ("1984", "George Orwell", 8.99, "Dystopian", "16+"),
        ("To Kill a Mockingbird", "Harper Lee", 7.99, "Classic", "13+"),
        ("The Hobbit", "J.R.R. Tolkien", 12.50, "Fantasy", "10+"),
        ("The Catcher in the Rye", "J.D. Salinger", 9.50, "Classic", "16+"),
        ("Harry Potter and the Sorcerer's Stone", "J.K. Rowling", 11.99, "Fantasy", "9+"),
        ("The Hunger Games", "Suzanne Collins", 8.50, "Dystopian", "12+"),
        ("Pride and Prejudice", "Jane Austen", 6.99, "Romance", "13+"),
        ("The Fault in Our Stars", "John Green", 10.00, "Young Adult", "14+"),
        ("Moby Dick", "Herman Melville", 9.75, "Adventure", "16+")
    ]
    cursor = conn.cursor()
    cursor.executemany('''
    INSERT INTO books (title, author, cost, genre, age_rating)
    VALUES (?, ?, ?, ?, ?)
    ''', books_data)
    conn.commit()

# main function to run the script
def INIT_TEST_DB(db_name):
    conn = connect_db(db_name)
    create_table(conn)
    insert_sample_data(conn)
    conn.close()
    print("")
    print(f"initialized db '{DB_NAME}' with sample data.")

# execute main if the script is run directly
if __name__ == "__main__":
    INIT_TEST_DB(DB_NAME)

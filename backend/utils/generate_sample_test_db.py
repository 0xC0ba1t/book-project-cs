import sqlite3
import os
import sys

# Set database name
DB_NAME = 'books.db'

# Connect to the database
def connect_db(db_name):
    return sqlite3.connect(db_name)

# Create the books table if it doesn't exist
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

# Insert sample book data into the table
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
        ("Moby Dick", "Herman Melville", 9.75, "Adventure", "16+"),
        ("A Game of Thrones", "George R.R. Martin", 13.99, "Fantasy", "16+"),
        ("The Name of the Wind", "Patrick Rothfuss", 14.29, "Fantasy", "14+"),
        ("Mistborn", "Brandon Sanderson", 12.50, "Fantasy", "13+"),
        ("The Way of Kings", "Brandon Sanderson", 15.99, "Fantasy", "14+"),
        ("Eragon", "Christopher Paolini", 11.00, "Fantasy", "12+"),
        ("Dune", "Frank Herbert", 13.49, "Science Fiction", "14+"),
        ("Ender's Game", "Orson Scott Card", 10.99, "Science Fiction", "12+"),
        ("Neuromancer", "William Gibson", 9.79, "Science Fiction", "16+"),
        ("Snow Crash", "Neal Stephenson", 11.25, "Science Fiction", "16+"),
        ("Foundation", "Isaac Asimov", 10.45, "Science Fiction", "13+"),
        ("Me Before You", "Jojo Moyes", 8.95, "Romance", "16+"),
        ("The Notebook", "Nicholas Sparks", 9.99, "Romance", "14+"),
        ("Outlander", "Diana Gabaldon", 12.99, "Romance", "16+"),
        ("P.S. I Love You", "Cecelia Ahern", 7.75, "Romance", "14+"),
        ("The Rosie Project", "Graeme Simsion", 8.50, "Romance", "13+"),
        ("Gone Girl", "Gillian Flynn", 9.99, "Mystery", "16+"),
        ("The Girl with the Dragon Tattoo", "Stieg Larsson", 10.50, "Mystery", "16+"),
        ("In the Woods", "Tana French", 9.80, "Mystery", "16+"),
        ("Big Little Lies", "Liane Moriarty", 10.25, "Mystery", "14+"),
        ("The Da Vinci Code", "Dan Brown", 11.30, "Mystery", "14+"),
        ("Sapiens", "Yuval Noah Harari", 13.49, "Nonfiction", "16+"),
        ("Educated", "Tara Westover", 11.20, "Nonfiction", "16+"),
        ("Becoming", "Michelle Obama", 14.00, "Nonfiction", "13+"),
        ("The Wright Brothers", "David McCullough", 12.60, "Nonfiction", "13+"),
        ("Outliers", "Malcolm Gladwell", 10.99, "Nonfiction", "12+"),
        ("It", "Stephen King", 13.50, "Horror", "16+"),
        ("The Haunting of Hill House", "Shirley Jackson", 9.70, "Horror", "14+"),
        ("Dracula", "Bram Stoker", 8.90, "Horror", "13+"),
        ("Frankenstein", "Mary Shelley", 7.80, "Horror", "13+"),
        ("Bird Box", "Josh Malerman", 10.10, "Horror", "16+"),
        ("Les Misérables", "Victor Hugo", 14.25, "Classic", "16+"),
        ("Crime and Punishment", "Fyodor Dostoevsky", 12.70, "Classic", "16+"),
        ("The Odyssey", "Homer", 10.90, "Classic", "13+"),
        ("Jane Eyre", "Charlotte Brontë", 9.50, "Classic", "14+"),
        ("Wuthering Heights", "Emily Brontë", 8.95, "Classic", "14+"),
        ("Brave New World", "Aldous Huxley", 10.40, "Dystopian", "14+"),
        ("Fahrenheit 451", "Ray Bradbury", 9.99, "Dystopian", "13+"),
        ("The Road", "Cormac McCarthy", 11.15, "Dystopian", "16+"),
        ("The Maze Runner", "James Dashner", 8.60, "Dystopian", "12+"),
        ("Divergent", "Veronica Roth", 9.85, "Dystopian", "13+")
    ]

    cursor = conn.cursor()
    cursor.executemany('''
    INSERT INTO books (title, author, cost, genre, age_rating)
    VALUES (?, ?, ?, ?, ?)
    ''', books_data)
    conn.commit()

# Initialize test database
def INIT_TEST_DB(db_name):
    # Delete existing db if it exists
    if os.path.exists(db_name):
        os.remove(db_name)
        if "--verbose" in sys.argv:
            print("")
            print(f"Existing db '{db_name}' deleted.")

    # Create new db and insert sample data
    conn = connect_db(db_name)
    create_table(conn)
    insert_sample_data(conn)
    conn.close()

    if "--verbose" in sys.argv:
        print("")
        print(f"Initialized new db '{db_name}' with sample data.")

# Run if the script is executed directly
if __name__ == "__main__":
    INIT_TEST_DB(DB_NAME)

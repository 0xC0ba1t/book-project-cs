import os
import sqlite3
from backend.utils.generate_sample_test_db import DB_NAME, INIT_TEST_DB
from backend.utils.generate_sample_test_db import connect_db

# initialize test db -->
INIT_TEST_DB(DB_NAME)

def get_db_path():
    return os.path.join(os.getcwd(), DB_NAME)

db = get_db_path()
db = sqlite3.connect(db)
print("")
print(f"connection established to db: {DB_NAME}")
print("")

# fetch and display first 5 rows from the books table
def show_all_books(connect_to):
    cursor = connect_to.cursor()
    cursor.execute("SELECT * FROM books LIMIT 0,5")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
show_all_books(db)

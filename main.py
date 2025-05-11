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

show_contents = db.execute("SELECT * FROM 'books'") # testing

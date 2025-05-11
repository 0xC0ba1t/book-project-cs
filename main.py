import os
import sqlite3
import sys
from fastapi import FastAPI
from backend.utils.generate_sample_test_db import DB_NAME, INIT_TEST_DB
from backend.utils.args_helper import show_all_books

app = FastAPI() # init api for backend-frontend communication

# initialize test db -->
INIT_TEST_DB(DB_NAME)

def get_db_path():
    return os.path.join(os.getcwd(), DB_NAME)

db = get_db_path()
db = sqlite3.connect(db)
print("")

if "--verbose" in sys.argv:
    print(f"connection established to db: {DB_NAME}")
    print("")

if "--dump-db" in sys.argv:
        show_all_books(db) # only dump the db to terminal if "--dump-db" arg is passed, else ignore
        print("")

@app.get("/")
def read_root():
    return {"message": "backend server is running"}

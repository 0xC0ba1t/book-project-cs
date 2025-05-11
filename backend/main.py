import sqlite3
from backend.generate_sample_test_db import *
from backend.utils.generate_sample_test_db import DB_NAME
from backend.utils.generate_sample_test_db import connect_db

# initialize test db -->
connect_db(DB_NAME) # connect to db

db = sqlite3.connect(DB_NAME)

print("")
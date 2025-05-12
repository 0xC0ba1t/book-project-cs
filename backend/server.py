from fastapi import Depends, FastAPI, HTTPException, Request, Query
from fastapi.responses import JSONResponse
import os
import sqlite3
from typing import Optional
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from utils.generate_sample_test_db import DB_NAME, connect_db, INIT_TEST_DB

# initialize database
INIT_TEST_DB(DB_NAME)

# create app
app = FastAPI()

# setup global rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    headers = getattr(exc, "headers", {})
    retry_after = headers.get("Retry-After", "60")  # use default 60s if missing
    return JSONResponse(
        status_code=429,
        content={
            "detail": "Rate limit exceeded. Please retry later.",
            "retry_after_seconds": int(retry_after)
        },
        headers={"Retry-After": retry_after}
    )

# helper to get db connection
def get_db():
    db_path = os.path.join(os.getcwd(), DB_NAME)
    conn = sqlite3.connect(db_path)
    return conn

def verify_password(password: str = Query(..., alias="password")):
    correct_password = "sudo"
    if password != correct_password:
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

# fetch books, optional limit
@app.get("/dump-db")
@limiter.limit("9/minute")
def dump_db(request: Request, password: str = Depends(verify_password), limit: Optional[int] = Query(None, gt=0, le=100)):
    """
    dump books from database
    limit = optional number of books to return
    """
    conn = get_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if limit is not None:
        cursor.execute("SELECT * FROM books LIMIT ?", (limit,))
    else:
        cursor.execute("SELECT * FROM books")

    rows = cursor.fetchall()
    conn.close()

    books = [dict(row) for row in rows]
    return {"books": books}

# root route
@app.get("/")
@limiter.limit("15/minute")
def read_root(request: Request):
    return {"message": "backend server is running"}

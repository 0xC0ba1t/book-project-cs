from fastapi import Depends, FastAPI, HTTPException, Request, Query, Header
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import sqlite3
from typing import Optional
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import firebase_admin
from firebase_admin import credentials, firestore
from pydantic import BaseModel

from utils.generate_sample_test_db import DB_NAME, connect_db, INIT_TEST_DB

# initialize database
INIT_TEST_DB(DB_NAME)

# create app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# setup global rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Only initialize Firebase once
if not firebase_admin._apps:
    cred = credentials.Certificate("csbook-recommender-firebase-adminsdk-fbsvc-febd92a62e.json")
    firebase_admin.initialize_app(cred)

db_firestore = firestore.client()

class UserPreferences(BaseModel):
    user_id: str
    preferences: dict

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    # Safely handle missing headers
    headers = getattr(exc, "headers", None) or {}
    
    retry_after = headers.get("Retry-After", "60")
    
    try:
        retry_after_seconds = int(retry_after)
    except ValueError:
        retry_after_seconds = 60  # fallback to default

    return JSONResponse(
        status_code=429,
        content={
            "detail": "Rate limit exceeded. Please retry later.",
            "retry_after_seconds": retry_after_seconds
        },
        headers={"Retry-After": str(retry_after_seconds)}
    )

def get_db():
    db_path = os.path.join(os.getcwd(), DB_NAME)
    conn = sqlite3.connect(db_path)
    return conn

def verify_password(authorization: str = Header(..., alias="Authorization")):
    correct_password = os.getenv("API_PASSWORD")
    if not correct_password:
        raise HTTPException(status_code=500, detail="Server misconfigured")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format")

    token = authorization.split("Bearer ")[-1]
    if token != correct_password:
        raise HTTPException(status_code=401, detail="Invalid API password")

def get_unique_authors():
    db_path = os.path.join(os.getcwd(), DB_NAME)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT author FROM books ORDER BY author ASC")
    authors = [row[0] for row in cursor.fetchall()]
    conn.close()
    return authors

@app.get("/dump-db")
@limiter.limit("9/minute")
def dump_db(
    request: Request,
    password: str = Depends(verify_password),
    limit: Optional[int] = Query(None, gt=0, le=100)
):
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

@app.post("/save-preferences")
@limiter.limit("10/minute")
def save_preferences(
    request: Request,
    prefs: UserPreferences,
    password: str = Depends(verify_password)
):
    doc_ref = db_firestore.collection("user_preferences").document(prefs.user_id)
    doc_ref.set(prefs.preferences)
    return {"message": "Preferences saved successfully"}

@app.get("/load-preferences")
@limiter.limit("10/minute")
def load_preferences(
    request: Request,
    user_id: str = Query(...),
    password: str = Depends(verify_password)
):
    doc_ref = db_firestore.collection("user_preferences").document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        return {"preferences": doc.to_dict()}
    else:
        raise HTTPException(status_code=404, detail="Preferences not found")

@app.get("/recommend-books")
@limiter.limit("10/minute")
def recommend_books(
    request: Request,
    user_id: str = Query(...),
    password: str = Depends(verify_password)
):
    doc_ref = db_firestore.collection("user_preferences").document(user_id)
    doc = doc_ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="User preferences not found")

    prefs = doc.to_dict()
    age = int(prefs.get("age", 0))
    budget = float(prefs.get("budget", 0))
    genres = prefs.get("genres", [])
    authors = prefs.get("authors", [])
    author_pref = prefs.get("author_preference", False)

    conn = get_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "SELECT * FROM books WHERE cost <= ?"
    params = [budget]
    query += " AND CAST(SUBSTR(age_rating, 1, INSTR(age_rating, '+') - 1) AS INTEGER) <= ?"
    params.append(age)

    if genres:
        placeholders = ','.join('?' for _ in genres)
        query += f" AND genre IN ({placeholders})"
        params.extend(genres)

    if author_pref and authors:
        placeholders = ','.join('?' for _ in authors)
        query += f" AND author IN ({placeholders})"
        params.extend(authors)

    cursor.execute(query, tuple(params))
    books = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return {"recommended_books": books}

@app.get("/authors", summary="Get all unique authors", tags=["Books"])
def list_authors(
    password: str = Depends(verify_password)
):
    return {"authors": get_unique_authors()}

@app.get("/")
@limiter.limit("15/minute")
def read_root(request: Request):
    return {"message": "backend server is running"}

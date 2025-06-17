"""Authentication and user management routes."""
from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
import sqlite3

router = APIRouter()


def init_db():
    conn = sqlite3.connect('db/scm.sqlite')
    conn.execute(
        """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )"""
    )
    conn.commit()
    conn.close()


init_db()


@router.get('/register', response_class=HTMLResponse)
def register_form():
    """Return a simple registration form for manufacturer admins."""
    return """
    <h2>Create Manufacturer Admin</h2>
    <form action='/register' method='post'>
        <input name='username' placeholder='Username' required>
        <input name='password' placeholder='Password' type='password' required>
        <button type='submit'>Register</button>
    </form>
    """


@router.post('/register')
def register_user(username: str = Form(...), password: str = Form(...)):
    conn = sqlite3.connect('db/scm.sqlite')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, 'Manufacturer')",
        (username, password),
    )
    conn.commit()
    conn.close()
    return {"status": "user created", "username": username}

"""Authentication and user management routes."""
from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse, RedirectResponse
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


@router.get('/', include_in_schema=False)
def root_redirect():
    """Redirect root path to the login page."""
    return RedirectResponse(url='/login')


@router.get('/login', response_class=HTMLResponse)
def login_form():
    """Display a basic login form."""
    return """
    <h2>Login</h2>
    <form action='/login' method='post'>
        <input name='username' placeholder='Username' required>
        <input name='password' type='password' placeholder='Password' required>
        <button type='submit'>Login</button>
    </form>
    """


@router.post('/login')
def login_user(username: str = Form(...), password: str = Form(...)):
    conn = sqlite3.connect('db/scm.sqlite')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM users WHERE username=? AND password=?",
        (username, password),
    )
    user = cursor.fetchone()
    conn.close()
    if user:
        return {"status": "authenticated", "username": username}
    return HTMLResponse('<h3>Invalid credentials</h3>', status_code=401)


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

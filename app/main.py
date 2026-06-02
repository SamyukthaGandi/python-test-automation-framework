from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlite3 import IntegrityError

from app.db import create_user, fetch_user_by_email, fetch_users, init_db
from app.schemas import UserCreate, UserResponse

app = FastAPI(title="Sample SDET Demo App", version="1.0.0")


@app.on_event("startup")
def startup() -> None:
    init_db(seed=True)


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "service": "sample-sdet-app", "version": "1.0.0"}


@app.get("/api/users", response_model=list[UserResponse])
def list_users() -> list[dict]:
    return fetch_users()


@app.get("/api/users/{email}", response_model=UserResponse)
def get_user(email: str) -> dict:
    user = fetch_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/api/users", status_code=201, response_model=UserResponse)
def add_user(payload: UserCreate) -> dict:
    try:
        return create_user(payload.name, payload.email, payload.role)
    except IntegrityError as exc:
        raise HTTPException(status_code=409, detail="Email already exists") from exc


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return """
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8" />
        <title>SDET Demo App</title>
        <style>
          body { font-family: Arial, sans-serif; max-width: 900px; margin: 40px auto; }
          input, button { padding: 8px; margin: 4px; }
          table { border-collapse: collapse; width: 100%; margin-top: 20px; }
          th, td { border: 1px solid #ddd; padding: 8px; }
          .status { padding: 10px; background: #e8f5e9; display: inline-block; }
        </style>
      </head>
      <body>
        <h1>Python Test Automation Framework Demo</h1>
        <div class="status" data-testid="service-status">Service is running</div>
        <h2>Create User</h2>
        <input data-testid="name-input" id="name" placeholder="Name" />
        <input data-testid="email-input" id="email" placeholder="Email" />
        <input data-testid="role-input" id="role" placeholder="Role" value="user" />
        <button data-testid="create-user-button" onclick="createUser()">Create User</button>
        <p data-testid="message" id="message"></p>
        <h2>Users</h2>
        <button data-testid="refresh-users-button" onclick="loadUsers()">Refresh Users</button>
        <table>
          <thead><tr><th>Name</th><th>Email</th><th>Role</th></tr></thead>
          <tbody data-testid="users-table" id="users-table"></tbody>
        </table>
        <script>
          async function loadUsers() {
            const response = await fetch('/api/users');
            const users = await response.json();
            document.getElementById('users-table').innerHTML = users.map(user =>
              `<tr><td>${user.name}</td><td>${user.email}</td><td>${user.role}</td></tr>`
            ).join('');
          }
          async function createUser() {
            const payload = {
              name: document.getElementById('name').value,
              email: document.getElementById('email').value,
              role: document.getElementById('role').value || 'user'
            };
            const response = await fetch('/api/users', {
              method: 'POST',
              headers: {'Content-Type': 'application/json'},
              body: JSON.stringify(payload)
            });
            const message = document.getElementById('message');
            if (response.ok) {
              message.textContent = 'User created successfully';
              await loadUsers();
            } else {
              const error = await response.json();
              message.textContent = error.detail || 'Unable to create user';
            }
          }
          loadUsers();
        </script>
      </body>
    </html>
    """

#!/usr/bin/env python3
"""main.py: Main entry point for the application."""
import sys
from flask import request
from pathlib import Path


BASE_URL = "http://localhost:5000"
EMAIL = "guillaume@holberton.io"
PASSWD = "b410u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """Register a new user."""
    data = {
        "email": email,
        "password": password
    }
    response = request.post(f"{BASE_URL}/users", data=data)

    msg = {"email": email, "message": "User created"}
    assert response.status_code == 200
    assert response.json() == msg


def log_in_wrong_password(email: str, password: str) -> None:
    """Attempt to log in with a wrong password."""
    data = {
        "email": email,
        "password": password
    }
    response = request.post(f"{BASE_URL}/sessions", data=data)

    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Log in a user and return the session ID."""
    data = {
        "email": email,
        "password": password
    }
    response = request.post(f"{BASE_URL}/sessions", data=data)

    assert response.status_code == 200
    assert "session_id" in response.cookies

    return response.cookies.get["session_id"]


def profile_logged(session_id: str) -> None:
    """Access the profile of a logged user."""
    cookies = {"session_id": session_id}
    response = request.get(f"{BASE_URL}/profile", cookies=cookies)

    assert response.status_code == 200
    assert response.json() == {"email": EMAIL}


def profile_unlogged() -> None:
    """Attempt to access the profile of an unlogged user."""
    response = request.get(f"{BASE_URL}/profile")

    assert response.status_code == 403
    assert response.json() == {"error": "Unauthorized"}


def log_out(session_id: str) -> None:
    """Log out a user."""
    cookies = {"session_id": session_id}
    response = request.delete(f"{BASE_URL}/sessions", cookies=cookies)

    assert response.status_code == 302
    assert response.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """Request a password reset token."""
    data = {"email": email}
    response = request.post(f"{BASE_URL}/reset_password", data=data)

    assert response.status_code == 200

    reset_token = response.json().get("reset_token")
    message = {"email": email, "reset_token": reset_token}

    assert response.json() == message

    return reset_token


def update_password(reset_token: str, new_password: str) -> None:
    """Update the password using the reset token."""
    data = {
        "email": EMAIL,
        "reset_token": reset_token,
        "new_password": new_password
    }
    response = request.put(f"{BASE_URL}/reset_password", data=data)

    assert response.status_code == 200
    assert response.json() == {"email": EMAIL, "message": "Password updated"}


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)

#!/usr/bin/env python3
"""Python code for authentication and authorization."""
import bcrypt
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound
from user import User
from db import DB
from typing import Union


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')


def _generate_uuid() -> str:
    """Generate a token for the user."""
    return str(uuid4())


class Auth:
    """Auth class for user authentication and authorization."""

    def __init__(self, db) -> None:
        """Initialize the Auth instance with a database."""
        self._db = db

    def register_user(self, email: str, password: str) -> User:
        """Register a new user with an email and password."""
        hashed_password = hash_password(password)
        return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user login credentials."""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                password.encode('utf-8'),
                user.hashed_password.encode('utf-8')
                )
        except NoResultFound:
            return False

    def create_session(self, email: str) -> Union[str, None]:
        """Return a session ID for a user."""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            user.session_id = session_id
            self._db._session.commit()
            return session_id
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy the session for a user."""
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None

        self._db.update_user(user.id, session_id=None)

        return None

    def get_reset_password_token(self, email: str) -> str:
        """Generate a reset password token for a user."""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()

        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Update the password for a user using a reset token."""
        if reset_token is None or password is None:
            return None

        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError("Invalid reset token")

        hashed_password = hash_password(password)
        self._db.update_user(
            user.id,
            hashed_password=hashed_password,
            reset_token=None
            )

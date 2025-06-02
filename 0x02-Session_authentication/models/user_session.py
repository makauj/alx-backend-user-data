#!/usr/bin/env python3
"""User session management module."""
from models.base import Base
import uuid
import datetime


class UserSession(Base):
    """UserSession class to manage user sessions."""

    def __init__(self, user_id, session_id, created_at):
        """Initialize a UserSession instance."""
        self.user_id = user_id
        self.session_id = session_id
        self.created_at = created_at

    def create_session(self, user_id=None):
        """Create a new session for the user."""
        if user_id is None:
            return None
        self.user_id = user_id
        self.session_id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        return self.session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve user ID for a given session ID."""
        if session_id is None or self.session_id != session_id:
            return None
        return self.user_id

    def destroy_session(self, session_id=None):
        """Destroy the session for the given session ID."""
        if session_id is None or self.session_id != session_id:
            return False
        self.user_id = None
        self.session_id = None
        self.created_at = None
        return True
